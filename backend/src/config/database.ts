import { Pool } from "pg";

function resolveSslConfig() {
  const sslMode = (process.env.DATABASE_SSL || "false").toLowerCase();
  if (["1", "true", "require", "on"].includes(sslMode)) {
    return { rejectUnauthorized: false };
  }
  return false;
}

const pool = new Pool({
  user: process.env.DATABASE_USER,
  host: process.env.DATABASE_HOST,
  database: process.env.DATABASE_NAME,
  password: process.env.DATABASE_PASSWORD,
  port: Number(process.env.DATABASE_PORT),
  ssl: resolveSslConfig(),
});

// test kết nối
(async () => {
  try {
    const res = await pool.query("SELECT NOW()");
    console.log("✅ Kết nối thành công, thời gian DB:", res.rows[0]);
  } catch (err) {
    console.error("❌ Lỗi kết nối:", err);
    console.log("DB CONFIG:", {
      user: process.env.DATABASE_USER,
      password: process.env.DATABASE_PASSWORD,
      host: process.env.DATABASE_HOST,
      port: process.env.DATABASE_PORT,
      database: process.env.DATABASE_NAME,
    });
  }
})();

// Hàm query chung
export const query = (text: string, params?: any[]) => {
  return pool.query(text, params);
};

export default pool;
