library(plyr)
library(tidyverse)
library(tidytext)
library(widyr)
library(igraph)
library(ggraph)
library(textdata)
library(data.table) 

dates <- seq(as.Date("2007-3-1"), by= "month", length.out = 175)

dates <- format(as.Date(dates), "%Y-%m")

custom_stop_words <- data_frame(word = c("rt", "htt", "https", "t.co", "@"), lexicon = "custom")


for (date in dates){
  df <- read.csv(paste(date, ".csv", sep = ""))
  df <- df[!duplicated(df),]
  
  df <- df %>% unnest_tokens(output = word, input = tweet) %>%
    anti_join(custom_stop_words, by = "word") %>%
    filter(str_detect(word, "[:alpha:]")) %>%
    distinct()
  
  df <- df %>% group_by(date, username) %>% 
    summarize(tweet = str_c(word, collapse = " ")) %>%
    ungroup()
  
  
  write.csv(df, paste(date,"_clean.csv", sep = ""), row.names = FALSE)
  
}


