import AWS from 'aws-sdk';
import createError from 'http-errors';
import validator from '@middy/validator';
import { getAuctionById } from './getAuction';
import commonMiddleware from '../lib/commonMiddleware';
import placeBidSchema from '../lib/schemas/placeBidSchema';

const dynamodb = new AWS.DynamoDB.DocumentClient();

async function placeBid(event, context) {
  const { id } = event.pathParameters;
  const { amount } = event.body;
  const { email, principalId } = event.requestContext.authorizer;

  const auction = await getAuctionById(id);
  // check if seller == bidder
  if (auction.sellerId === principalId) {
    throw new createError.Forbidden('You cannot bid on your own auctions!');
  }
  // check if double bid
  if (auction.highestBid.id === principalId) {
    throw new createError.Forbidden('You are already the highest bidder.');
  }
  // check if auction is closed
  if (auction.status !== 'OPEN') {
    throw new createError.Forbidden(`The auction is closed`);
  }
  // check if bid amount > currently highest bid amount
  if (amount <= auction.highestBid.amount) {
    throw new createError.Forbidden(`Your bid must be higher than ${auction.highestBid.amount}`);
  }

  const params = {
    TableName: process.env.AUCTIONS_TABLE_NAME,
    Key: { id },
    UpdateExpression: 'set highestBid.amount = :amount, highestBid.id = :bidderId, highestBid.email = :bidderEmail',
    ExpressionAttributeValues: {
      ':amount': amount,
      ':bidderId': principalId,
      ':bidderEmail': email
    },
    ReturnValues: 'ALL_NEW'
  };

  let updatedAuction;

  try {
    const result = await dynamodb.update(params).promise();
    updatedAuction = result.Attributes;
  } catch (error) {
    console.log(error);
    throw new createError.InternalServerError(error);
  }

  return {
    statusCode: 200,
    body: JSON.stringify(updatedAuction),
  };
}

export const handler = commonMiddleware(placeBid)
  .use(validator({ inputSchema: placeBidSchema }));