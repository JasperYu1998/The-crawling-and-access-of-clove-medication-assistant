USE zeyu_test;
SET @@global.sql_mode= '';
DROP TABLE IF EXISTS `Medicines`;
CREATE TABLE Medicines(
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
`type1` VARCHAR(255) COMMENT '类别1',
`type2`  VARCHAR(255) COMMENT '类别2',
`general_name` VARCHAR(255) COMMENT "通用名称" ,
`English_name` VARCHAR(255) COMMENT "英文名称",
`product_name` VARCHAR(255) COMMENT "商品名称" ,
`company` VARCHAR(255) COMMENT "公司名",
`component` VARCHAR(255) COMMENT "成份",
`indication` VARCHAR(255) COMMENT "适应症",
`dosage` VARCHAR(255) COMMENT "用法用量",
`ban` VARCHAR(255) COMMENT "禁忌",
`warn` VARCHAR(255) COMMENT "警告",
`notice` VARCHAR(255) COMMENT "注意事项", 
`women` VARCHAR(255) COMMENT "孕妇及哺乳期妇女用药",
`pharmacology` VARCHAR(255) COMMENT "药理作用",
`dynamics` VARCHAR(255) COMMENT "药代动力学",
 `OTC` VARCHAR(255) COMMENT "是否OTC",
 `date_verify` VARCHAR(255) COMMENT "核准日期",
 `date_alter`VARCHAR(255) COMMENT "修改日期",
 `Toxicology`VARCHAR(255) COMMENT "毒理研究",
 `component_che` VARCHAR(255) COMMENT "化学成份",
 `class` VARCHAR(255) COMMENT "药品监管分级",
 `over_instruct` VARCHAR(255) COMMENT "超说明书适应症",
 `experiment` VARCHAR(255) COMMENT "临床试验",
 `drug_and_food` VARCHAR(255) COMMENT "服药与进食",
 `medication_instructions` VARCHAR COMMENT "用药须知",
  `other` VARCHAR(255) COMMENT "其他未列类别",
 PRIMARY KEY (`id`)
  )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='丁香园药品表';
