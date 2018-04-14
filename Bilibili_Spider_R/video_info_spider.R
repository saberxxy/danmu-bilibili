# 抓取B站视频信息

library(jsonlite)
library(RMySQL)
library(parallel)

# 返回值格式
# "data":
# {
#     "aid": "av号",
#     "view": "播放数",
#     "danmaku": "弹幕数",
#     "reply": "评论数",
#     "favorite": "收藏数",
#     "coin": "硬币数",
#     "share": "分享数",
#     "now_rank": "现排行",
#     "his_rank": "最高全站日排名（0表示未曾上榜)",
#     "no_reprint": "0表示默认 1表示未经作者授权禁止转载",
#     "copyright": "1表示原创 2表示搬运"
# }

# 首先判断返回的code，如果为0，则代表该av号有视频，否则无视频
# is_ok <- function(code) {
#     if (code == 0) {
#         return ("TRUE")
#     } else {
#         return ("FALSE")
#     }  
# }

# 根据目前的经验，B站视频av号从7开始到2千万
get_video_info <- function(id) {
    base_url <- "http://api.bilibili.com/x/web-interface/archive/stat?aid="
    url <- paste(base_url, as.character(id), sep="")
    content <- jsonlite::fromJSON(url)
    code <- content$code
    if (code == 0) {
        # "aid": "av号",
        aid <- content$data$aid
        # "view": "播放数",
        view <- content$data$view
        # "danmaku": "弹幕数",
        danmaku <- content$data$danmaku
        # "reply": "评论数",
        reply <- content$data$reply
        # "favorite": "收藏数",
        favorite <- content$data$favorite
        # "coin": "硬币数",
        coin <- content$data$coin
        # "share": "分享数",
        share <- content$data$share
        # "now_rank": "现排行",
        now_rank <- content$data$now_rank
        # "his_rank": "最高全站日排名（0表示未曾上榜)",
        his_rank <- content$data$his_rank
        # "no_reprint": "0表示默认 1表示未经作者授权禁止转载",
        no_reprint <- content$data$no_reprint
        # "copyright": "1表示原创 2表示搬运"
        copyright <- content$data$copyright
        
        # video_info <- c(aid,view,danmaku,reply,favorite,coin,
        #                 share,now_rank,his_rank,no_reprint,copyright)
        
        
        # basics <- dbGetQuery(conn, "SELECT * FROM bilibili_video_info")
        # dbSendUpdate(conn, sql)
        # dbSendUpdate(conn, "commit")
        sql_str <- paste("insert into bilibili_video_info(aid, view, danmaku, reply,",
                         "favorite, coin, share, now_rank, his_rank, no_reprint, copyright",
                         ") values('", aid, "','", view,"','", danmaku, "','",
                         reply, "','", favorite, "','", coin, "','", share, "','", 
                         now_rank, "','", his_rank, "','", no_reprint, "','", copyright, "')", sep="")
        RMySQL::dbSendQuery(conn, sql_str)
        RMySQL::dbCommit(conn)
        # RMySQL::dbDisconnect(conn)
        cat(id, '插入成功，')
        
        # 生成随机数，休息，防止请求太猛被干掉
        sleep_time <- runif(1, min=0, max=3)
        cat('休息', sleep_time, 's\n')
        Sys.sleep(sleep_time)
    } 

}


# 程序入口

conn <- RMySQL::dbConnect(MySQL(), host='127.0.0.1', port=3306,
                  dbname="test", username="root", password="123456")

# 循环写法
# for (id in x_list) {
#     get_video_info(id)
# }
# 批处理方案
x_list <- 40527:3000000
lapply(x_list, get_video_info)
RMySQL::dbDisconnect(conn)
# 并行方案
# system.time({
#     cl.cores <- detectCores()
#     cl <- makeCluster(8)  # 初始化四核心集群
#     parLapply(cl, x_list, get_video_info)  # lapply的并行版本
#     stopCluster(cl)  # 关闭集群
# })


