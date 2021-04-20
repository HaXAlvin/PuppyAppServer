use puppy;
CREATE TABLE `data`(
    `id` INT UNSIGNED NOT NULL,
    -- 流水號
    `plan` VARCHAR(64) NOT NULL,
    -- 計畫編號
    `user` VARCHAR(64) NOT NULL,
    -- 訪員編號
    `img` LONGTEXT NOT NULL,
    -- 圖
    `lon` DOUBLE NOT NULL,
    -- 經
    `lat` DOUBLE NOT NULL,
    -- 緯
    `city` VARCHAR(128) CHARACTER SET utf8mb4 NOT NULL,
    -- 縣 / 直轄市 / 市
    `district` VARCHAR(128) CHARACTER SET utf8mb4 NOT NULL,
    -- 鄉 / 鎮 / 區 / 縣轄市
    `village` VARCHAR(128) CHARACTER SET utf8mb4 NOT NULL,
    -- 村 / 里
    `date` TIMESTAMP NOT NULL,
    -- 照片時間
    `dayCount` INT UNSIGNED NOT NULL,
    -- 調查天數
    `dogCount` INT UNSIGNED NOT NULL,
    `repeatCount` INT UNSIGNED NOT NULL,
    PRIMARY KEY(`plan`, `user`, `id`)
);
CREATE TABLE `user`(
    `plan` VARCHAR(64) NOT NULL,
    `user` VARCHAR(64) NOT NULL,
    `name` VARCHAR(128) CHARACTER SET utf8mb4,
    PRIMARY KEY(`user`,`plan`)
);
CREATE TABLE `timingLocation`(
    `plan` VARCHAR(64) NOT NULL,
    `user` VARCHAR(64) NOT NULL ,
    `time` timestamp not null,
    `lon` DOUBLE NOT NULL,
    -- 經
    `lat` DOUBLE NOT NULL
    -- 緯
);
# CREATE TABLE `join_plan` (
#     `plan` INT NOT NULL,
#     `user` INT NOT NULL,
#     `count` INT NOT NULL DEFAULT 0,
#     PRIMARY KEY(`user`, `plan`)
# )