/*queue*/
CREATE TABLE queue
  (
    `id`          INT auto_increment NOT NULL,
    `priority`    INT DEFAULT 0,
    `type`        VARCHAR(64) NOT NULL,
    `min`         VARCHAR(64),
    `max`         VARCHAR(64),
    `started` DATETIME,
    `finished` DATETIME,
    PRIMARY KEY (id)
  );

CREATE TABLE errors
  (
    `id`     INT auto_increment NOT NULL,
    `state`  VARCHAR(64) NOT NULL,
    `error`  TEXT,
    `source` INT NOT NULL,
    PRIMARY KEY (id)
  );

/*FetchLog*/
CREATE TABLE fetchlog
  (
    `id`           INT auto_increment NOT NULL,
    `recordsadded` INT NOT NULL DEFAULT 0,
    `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `source`       INT NOT NULL,
    FOREIGN KEY (source) references queue(id) on delete cascade,
    PRIMARY KEY (id)
  );
