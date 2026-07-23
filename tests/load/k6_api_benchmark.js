import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api/v1';

export default function () {
  const resMeals = http.get(`${BASE_URL}/meals`);
  check(resMeals, {
    'meals status is 200 or 401': (r) => r.status === 200 || r.status === 401,
  });

  const resDaily = http.get(`${BASE_URL}/analytics/daily`);
  check(resDaily, {
    'daily analytics status is 200 or 401': (r) => r.status === 200 || r.status === 401,
  });

  sleep(1);
}
