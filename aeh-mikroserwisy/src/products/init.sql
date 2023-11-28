CREATE USER 'products_user'@'localhost' IDENTIFIED BY 'products123';

CREATE DATABASE products;

GRANT ALL PRIVILEGES ON products.* TO 'products_user'@'%' WITH GRANT OPTION;

USE products;

CREATE TABLE products (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  price INT NOT NULL,
  description VARCHAR(255) NOT NULL
);

INSERT INTO products (name, price, description) VALUES ('Okulary', '100', 'Okulary do czytania');
INSERT INTO products (name, price, description) VALUES ('TV', '2000', 'TV 4K');

  




