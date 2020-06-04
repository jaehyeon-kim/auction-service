import { v4 as uuid } from 'uuid';
import AWS from 'aws-sdk';

// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB/DocumentClient.html

const dynamodb = new AWS.DynamoDB.DocumentClient();

async function createAuction(event, context) {
  console.log(event.body);
  const { title } = JSON.parse(event.body);
  const now = new Date();

  const auction = {
    id: uuid(),
    title: title,
    status: 'OPEN',
    createdAt: now.toISOString(),
  };

  await dynamodb.put({
    TableName: process.env.AUCTIONS_TABLE_NAME,
    Item: auction,
  }).promise();

  return {
    statusCode: 201,
    body: JSON.stringify(auction),
  };
}

export const handler = createAuction;