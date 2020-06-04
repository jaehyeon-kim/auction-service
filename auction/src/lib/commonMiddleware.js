import middy from '@middy/core';
import httpJsonBodyParser from '@middy/http-json-body-parser';
import httpEventNormalizer from '@middy/http-event-normalizer';
import httpErrorHandler from '@middy/http-error-handler';

// this may be used as a replacement of @middy/http-error-handler
// https://github.com/dbartholomae/middy-middleware-json-error-handler

export default handler => middy(handler)
  .use([
    httpJsonBodyParser(),
    httpEventNormalizer(),
    httpErrorHandler()
  ]);