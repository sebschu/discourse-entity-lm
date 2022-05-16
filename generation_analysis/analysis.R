
library(tidyverse)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
theme_set(theme_bw())

d = read.csv("annotations_round1.csv")



d2 = d %>% 
  mutate(modal_order = case_when(grepl("negation_affirmative", id) ~ 2,
                                 grepl("failed_managed", id) ~ 2,
                                 grepl("doubt_know", id) ~ 2,
                                 grepl("modal_affirmative", id) ~ 2,
                                 TRUE ~ 1)) %>%
  mutate(enoun_coref = case_when(order == 1 & modal_order == 1 ~ Noun.1.COREF, 
                                 order == 2 & modal_order == 2 ~ Noun.1.COREF, 
                                 TRUE ~  Noun.2.COREF),
         nenoun_coref = case_when(order == 1 & modal_order == 1 ~ Noun.2.COREF, 
                                  order == 2 & modal_order == 2 ~ Noun.2.COREF, 
                                  TRUE ~  Noun.1.COREF),
         enoun_new = case_when(order == 1 & modal_order == 1 ~ Noun.1.NEW, 
                               order == 2 & modal_order == 2 ~ Noun.1.NEW, 
                               TRUE ~  Noun.2.NEW),
         nenoun_new = case_when(order == 1 & modal_order == 1 ~ Noun.2.NEW, 
                                  order == 2 & modal_order == 2 ~ Noun.2.NEW, 
                                  TRUE ~  Noun.1.NEW),
         enoun_modal = case_when(order == 1 & modal_order == 1 ~ Noun.1.MODAL, 
                                 order == 2 & modal_order == 2 ~ Noun.1.MODAL, 
                                 TRUE ~  Noun.2.MODAL),
         nenoun_modal = case_when(order == 1 & modal_order == 1 ~ Noun.2.MODAL, 
                                  order == 2 & modal_order == 2 ~ Noun.2.MODAL, 
                                  TRUE ~  Noun.1.MODAL)
         ) %>%
  mutate(type = case_when(
    type == "negation_affirmative" ~ "affirmative_negation",
    type == "modal_affirmative" ~ "affirmative_modal",
    type == "doubt_know" ~ "know_doubt",
    type == "failed_managed" ~ "managed_failed",
    TRUE ~ type))

d2 %>% group_by(type,  model) %>% 
  summarise(e_coref_prop=mean(enoun_coref), 
            ne_coref_prop = mean(nenoun_coref),
            e_new_prop = mean(enoun_new),
            ne_new_prop = mean(nenoun_new),
            e_modal_prop = mean(enoun_modal),
            ne_modal_prop = mean(nenoun_modal),
            amb_prop = mean(Ambiguous.COREF),
            neither_prop = mean(Neither.mentioned)
            )
 
d2 %>% group_by( model) %>% 
  summarise(e_coref_prop=mean(enoun_coref), 
            ne_coref_prop = mean(nenoun_coref),
            e_new_prop = mean(enoun_new),
            ne_new_prop = mean(nenoun_new),
            e_modal_prop = mean(enoun_modal),
            ne_modal_prop = mean(nenoun_modal),
            amb_prop = mean(Ambiguous.COREF),
            neither_prop = mean(Neither.mentioned)
  )

d2 %>% 
   pivot_longer(
     cols = ends_with("_coref")
   ) %>%
   ggplot(aes(x=name, fill=value)) + geom_histogram(stat="count") + facet_grid(type~model)
 

d2 %>% 
  pivot_longer(
    cols = ends_with("_new")
  ) %>%
  ggplot(aes(x=name, fill=value)) + geom_histogram(stat="count") + facet_grid(type~model)

