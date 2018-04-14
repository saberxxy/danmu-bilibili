# 分析视频信息

library(RMySQL)
library(jsonlite)
library(ggplot2)


# print(head(v_data))

# 本福特定律验证函数
ben <- function(data_list){
    data_list_first <- substring(data_list, 1, 1)
    data_list_first_table <- table(data_list_first)
    new_data_list_first <- data.frame(number=names(data_list_first_table), 
                           count=as.numeric(data_list_first_table))
    # ggplot(new_data_list_first,aes(x = number, y = count)) + 
    #     geom_bar(stat = "identity", fill = "lightblue", colour = "black")
    
    # 总频数
    sum_frequency <- sum(as.numeric(data_list_first_table))
    # 百分数频数分布
    frequency_pre_list <- 0
    frequency_pre_list <- as.numeric(data_list_first_table)/sum_frequency*100
    frequency_pre_data_frame <- data.frame(number = names(data_list_first_table),
                                        frequency = frequency_pre_list)
    # 频数百分数分布的data.frame
    print (frequency_pre_data_frame)
}


# 程序入口
conn_mysql <- RMySQL::dbConnect(MySQL(), host='127.0.0.1', port=3306,
                                dbname="test", username="root", password="123456")

v <- RMySQL::dbSendQuery(conn_mysql, 
                           "select * from bilibili_video_info 
                            where view <>'--' and danmaku<>'0'
                            and reply <> '0' and favorite<>'0'
                            and coin<>'0' and share <>'0'")
v_data <- RMySQL::dbFetch(v, n=-1)
RMySQL::dbDisconnect(conn_mysql)

# 播放量
data_list <- v_data$view
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")


# 弹幕数
data_list <- v_data$danmaku
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")


# 评论数
data_list <- v_data$reply
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")


# 收藏数
data_list <- v_data$favorite
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")


# 硬币数
data_list <- v_data$coin
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")


# 分享数
data_list <- v_data$share
ben(data_list)
data_list_first <- substring(data_list, 1, 1)
data_list_first_table <- table(data_list_first)
new_data_list_first <- data.frame(number=names(data_list_first_table), 
                                  count=as.numeric(data_list_first_table))
ggplot(new_data_list_first,aes(x = number, y = count)) + 
    geom_bar(stat = "identity", fill = "lightblue", colour = "black")
