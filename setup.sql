-- 创建打卡数据表
CREATE TABLE checkin_data (
  id INT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  data JSONB NOT NULL DEFAULT '{"tasks":{},"plan":{}}'::jsonb,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 插入初始数据
INSERT INTO checkin_data (id, data) VALUES (1, '{"tasks":{},"plan":{}}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 开启 RLS（行级安全）
ALTER TABLE checkin_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_all" ON checkin_data FOR ALL USING (true);
