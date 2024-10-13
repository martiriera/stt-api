CREATE_TRANSCRIPTION_TABLE = (
  "CREATE TABLE IF NOT EXISTS transcriptions ("
  "id UUID PRIMARY KEY DEFAULT gen_random_uuid(),"
  "text TEXT NOT NULL,"
  "created_at TIMESTAMP NOT NULL DEFAULT NOW()"
  ")"
)

INSERT_TRANSCRIPTION = (
  "INSERT INTO transcriptions (text) VALUES (%s) RETURNING id"
)
