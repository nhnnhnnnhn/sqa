# sqa

## Yêu cầu

- Cài `Node.js` và `npm`
- Cài `Docker` và `Docker Compose`

## Cài đặt và chạy dự án

### 1. Backend

Di chuyển vào thư mục `backend` và khởi động các service bằng Docker trước:

```bash
cd backend
docker compose up -d
```

Sau khi Docker chạy xong, cài dependency và start backend:

```bash
npm i
npm start
```

### 2. Frontend User

Mở terminal mới, di chuyển vào thư mục `frontend_user`, cài dependency, build rồi start:

```bash
cd frontend_user
npm i
npm run build
npm run start
```

### 3. Frontend Admin

Mở terminal mới khác, di chuyển vào thư mục `frontend_admin`, cài dependency, build rồi start:

```bash
cd frontend_admin
npm i
npm run build
npm run start
```

## Ghi chú

- Chạy mỗi phần ở một terminal riêng để tiện theo dõi log.
- `backend` cần chạy `docker compose up -d` trước khi `npm i && npm start`.
- `frontend_user` chạy production mode bằng `npm run build && npm run start`.
- `frontend_admin` chạy production mode bằng `npm run build && npm run start`.
