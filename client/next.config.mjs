
import dotenv from 'dotenv';

dotenv.config({ path: '../.env' });

/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
      domains: ['answers-embed-client.ufc.com.pagescdn.com', 'dmxg5wxfqgb4u.cloudfront.net'],
    },
    
  };

  
export default nextConfig;
