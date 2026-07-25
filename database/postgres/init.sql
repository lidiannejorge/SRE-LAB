CREATE TABLE IF NOT EXISTS clientes (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(100) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


CREATE TABLE IF NOT EXISTS pedidos (

    id SERIAL PRIMARY KEY,

    cliente_id INTEGER NOT NULL,

    produto VARCHAR(100),

    valor NUMERIC(10,2),

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


INSERT INTO clientes (nome,email)
VALUES
('Cliente Teste','teste@email.com')
ON CONFLICT DO NOTHING;


INSERT INTO pedidos(cliente_id,produto,valor)
VALUES
(1,'Notebook',3500.00);
