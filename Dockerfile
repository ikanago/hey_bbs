FROM node:14-buster-slim as frontend

WORKDIR /app

COPY frontend/yarn.lock frontend/package.json frontend/tsconfig.json ./

RUN yarn install --pure-lockfile

COPY frontend/public ./public/

COPY frontend/src ./src/

RUN yarn build

FROM python:3.8-slim

WORKDIR /app

RUN pip install pipenv

COPY backend/Pipfile.lock ./

RUN pipenv sync

COPY backend/libbbs ./libbbs/

COPY backend/main.py backend/model.py ./

COPY --from=frontend /app/build ./build/

CMD [ "pipenv", "run", "python", "main.py" ]
