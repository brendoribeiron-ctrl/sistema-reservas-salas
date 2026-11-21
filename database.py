"""by brendo
essa parte do db eu tive que pedir uma ajuda para montar om código
mas modelei ele no drawdb.app
dps exportei em código sql
o arquivo está na pasta
"""

import sqlite3

db_path = "dados.sqlite3"


def conexao():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = conexao()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS "usuarios" (
	"id_usuario" INTEGER NOT NULL,
	"matricula" TEXT NOT NULL UNIQUE,
	"nome_usuario" TEXT NOT NULL,
	"tipo" TEXT NOT NULL CHECK ("tipo" IN ('aluno', 'professor', 'admin')),
	"cpf" TEXT UNIQUE CHECK ("cpf" IS NULL OR (length("cpf") = 11 AND "cpf" NOT GLOB '*[^0-9]*')),
	"senha_hash" TEXT NOT NULL,
	PRIMARY KEY("id_usuario")
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS "salas" (
	"id_sala" INTEGER NOT NULL,
	"nome_sala" TEXT NOT NULL UNIQUE,
	"capacidade" INTEGER NOT NULL CHECK ("capacidade" > 0),
	"ativa" INTEGER NOT NULL DEFAULT 1 CHECK ("ativa" IN (0, 1)),
	PRIMARY KEY("id_sala")
    )
""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS "disciplinas" (
	"id_disciplina" INTEGER NOT NULL,
	"nome_disciplina" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_disciplina")
    )
""")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS "reservas" (
	"id_reserva" INTEGER NOT NULL,
	"id_sala" INTEGER NOT NULL,
	"id_usuario" INTEGER NOT NULL,
	"id_disciplina" INTEGER,
	"horario_inicio" TEXT NOT NULL,   -- ISO: 'AAAA-MM-DD HH:MM'
	"horario_final" TEXT NOT NULL,    -- ISO: 'AAAA-MM-DD HH:MM'
	"status" TEXT NOT NULL DEFAULT 'ativa' CHECK ("status" IN ('ativa', 'cancelada')),
	PRIMARY KEY("id_reserva"),
	CHECK ("horario_final" > "horario_inicio"),
	FOREIGN KEY ("id_sala") REFERENCES "salas"("id_sala") ON UPDATE CASCADE ON DELETE RESTRICT,
	FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario") ON UPDATE CASCADE ON DELETE RESTRICT,
	FOREIGN KEY ("id_disciplina") REFERENCES "disciplinas"("id_disciplina") ON UPDATE CASCADE ON DELETE SET NULL
    )
""")
    conn.execute("""
    CREATE INDEX IF NOT EXISTS "idx_reservas_sala_horario" ON "reservas"("id_sala", "horario_inicio", "horario_final")
""")
    conn.execute(
        """CREATE INDEX IF NOT EXISTS "idx_reservas_usuario" ON "reservas"("id_usuario")"""
    )

#bloco de verificação de conflito
#dispara um trigger e faz a verificação buscando conflitos nas datas marcadas
#roda antes de inserir reservas 
    conn.execute("""
    CREATE TRIGGER IF NOT EXISTS "trg_reservas_conflito_insert"  
    BEFORE INSERT ON "reservas"
    WHEN NEW."status" = 'ativa' AND EXISTS (
        SELECT 1 FROM "reservas" r
        WHERE r."id_sala" = NEW."id_sala"
        AND r."status" = 'ativa'
        AND NEW."horario_inicio" < r."horario_final"
        AND NEW."horario_final" > r."horario_inicio"

    )
    BEGIN
        SELECT RAISE(ABORT, 'Conflito de horario: sala ja reservada');
    END
    """)
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    conn = conexao()
    print(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    conn.close()
