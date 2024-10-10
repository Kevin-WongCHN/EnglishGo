import initSqlJs from "sql.js";

const dbbuf={}

export async function loadDb(db,path) {
  // 初始化 sql.js
  if (dbbuf[db]) {
    return dbbuf[db];
  }
  const SQL = await initSqlJs({
    locateFile: (file) => `https://sql.js.org/dist/${file}`,
  });
  // 从 public 文件夹中获取 .db 文件
  const response = await fetch(path);
  const buffer = await response.arrayBuffer();
  // 加载数据库
  let dbInstance = new SQL.Database(new Uint8Array(buffer));
  dbbuf[db] = dbInstance;
  return dbInstance;

}
