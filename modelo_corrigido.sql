--feito no drawdb

CREATE TABLE IF NOT EXISTS "usuarios" (
	"id_usuario" INTEGER NOT NULL,
	"matricula" TEXT NOT NULL UNIQUE,
	"nome_usuario" TEXT NOT NULL,
	"tipo" TEXT NOT NULL CHECK ("tipo" IN ('aluno', 'professor', 'admin')),
	"cpf" TEXT UNIQUE CHECK ("cpf" IS NULL OR (length("cpf") = 11 AND "cpf" NOT GLOB '*[^0-9]*')),
	"senha_hash" TEXT NOT NULL,
	PRIMARY KEY("id_usuario")
);

CREATE TABLE IF NOT EXISTS "salas" (
	"id_sala" INTEGER NOT NULL,
	"nome_sala" TEXT NOT NULL UNIQUE,
	"capacidade" INTEGER NOT NULL CHECK ("capacidade" > 0),
	"ativa" INTEGER NOT NULL DEFAULT 1 CHECK ("ativa" IN (0, 1)),
	PRIMARY KEY("id_sala")
);

CREATE TABLE IF NOT EXISTS "disciplinas" (
	"id_disciplina" INTEGER NOT NULL,
	"nome_disciplina" TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_disciplina")
);

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
);

CREATE INDEX IF NOT EXISTS "idx_reservas_sala_horario" ON "reservas"("id_sala", "horario_inicio", "horario_final");
CREATE INDEX IF NOT EXISTS "idx_reservas_usuario" ON "reservas"("id_usuario");
