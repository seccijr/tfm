import pandas as pd

df_inter = pd.read_csv('data\\mind_1M_dev\\mind_1M_dev.inter', '\t')
df_item = pd.read_csv('data\\mind_1M_dev\\mind_small_dev.item', '\t')
df_link = pd.read_csv('data\\mind_1M_dev\\mind_small_dev.link', '\t')
df_kg = pd.read_csv('data\\mind_1M_dev\\mind_small_dev.kg', '\t')
df_item_filtered = df_item[df_item['item_id:token'].isin(df_inter['item_id:token'])]
df_item_filtered.to_csv('data\\mind_1M_dev\\mind_1M_dev.item', '\t', index=False)
df_link_filtered = df_link[df_link['entity_id:token'].isin(df_item_filtered['entity_id:token'])]
df_link_filtered.to_csv('data\\mind_1M_dev\\mind_1M_dev.link', '\t', index=False)
df_kg_filtered = df_kg[df_kg['head_id:token'].isin(df_link_filtered['entity_id:token'])]
df_kg_filtered.to_csv('data\\mind_1M_dev\\mind_1M_dev.kg', '\t', index=False)