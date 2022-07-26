import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';

export default app => {
  app.use(cors());
  app.use(bodyParser.json({ limit: '20mb' }));
  app.use(bodyParser.urlencoded({ limit: '20mb', extended: true }));
  app.use(express.json());
};
