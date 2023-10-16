CREATE TABLE hyperwallet_paypal_0 (
    t_id VARCHAR(40) PRIMARY KEY,
    h_id CHAR(100),
    b_id CHAR(100),
    email CHAR(255),
    c_time INT(11),
    country CHAR(50),
    status INT(2) DEFAULT 1,
    firstname CHAR(255),
    lastname CHAR(255),
    birth_date INT(11),
    address1 CHAR(255),
    city CHAR(100),
    state_provice CHAR(50),
    postalcode CHAR(20),
    type CHAR(20),
    branchId CHAR(50),
    bankAccountId CHAR(50),
    bankAccountPurpose CHAR(20),
    INDEX idx_email (email)
);

CREATE INDEX idx_email ON hyperwallet_paypal_0 (email);
