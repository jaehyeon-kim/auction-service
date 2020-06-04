import { v4 as uuid } from 'uuid';
import AWS from 'aws-sdk';
import commonMiddleware from '../lib/commonMiddleware';
import createError from 'http-errors';

// const AWS = require('aws-sdk');
// const uuid = require('uuid');
// uuid.v4();

// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB/DocumentClient.html

const dynamodb = new AWS.DynamoDB.DocumentClient();

async function createAuction(event, context) {
  console.log(event.body);
  const { title } = event.body;
  // const { title } = JSON.parse(event.body);
  const now = new Date();

  const auction = {
    id: uuid(),
    title: title,
    status: 'OPEN',
    createdAt: now.toISOString(),
    highestBid: {
      amount: 0
    }
  };

  try {
    await dynamodb.put({
      TableName: process.env.AUCTIONS_TABLE_NAME,
      Item: auction,
    }).promise();
  } catch (error) {
    console.log(error);
    throw new createError.InternalServerError(error);
  }

  return {
    statusCode: 201,
    body: JSON.stringify(auction),
  };
}

export const handler = commonMiddleware(createAuction);
