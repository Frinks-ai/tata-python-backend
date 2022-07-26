require('dotenv').config();

const config = {
  PORT: process.env.PORT || 9000,
  DEVIATION: process.env.DEVIATION,
  BASE_PATH: process.env.BASE_PATH
};
export default config;
