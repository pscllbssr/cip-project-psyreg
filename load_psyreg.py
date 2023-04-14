import json
import pandas as pd

with open('data/psyreg_index.json', 'r') as f:
    data = json.load(f)

df = pd.json_normalize(data, meta=['id', 'name', 'firstName'], record_path=['cetTitles'], sep="_")

df = df.explode('permissions')

permissions_flat = df['permissions'].apply(pd.Series)['canton'].apply(pd.Series).add_prefix('permission_')
df = pd.concat([df.drop(['permissions'], axis=1), permissions_flat], axis=1)

df['link'] = df.id.apply(lambda id: 'https://www.healthreg-public.admin.ch/psyreg/person/{}'.format(id))

# have id and name as first columns
column_order = ['id', 'name', 'firstName', 'link', 'providers90Days', 'profession_id', 'profession_parentId',
                'profession_isActive', 'profession_textDe', 'profession_textFr', 'profession_textIt',
                'profession_textEn', 'profession_isNada', 'profession_isBgmd',
                'profession_isEquivalent', 'profession_isFederal', 'profession_isAcknowledgement', 'cetTitleType_id',
                'cetTitleType_parentId', 'cetTitleType_isActive', 'cetTitleType_textDe', 'cetTitleType_textFr',
                'cetTitleType_textIt', 'cetTitleType_textEn', 'cetTitleType_isNada', 'cetTitleType_isBgmd',
                'cetTitleType_isEquivalent', 'cetTitleType_isFederal', 'cetTitleType_isAcknowledgement',
                'cetTitleKind_id', 'cetTitleKind_parentId', 'cetTitleKind_isActive', 'cetTitleKind_textDe',
                'cetTitleKind_textFr', 'cetTitleKind_textIt', 'cetTitleKind_textEn', 'cetTitleKind_isNada',
                'cetTitleKind_isBgmd', 'cetTitleKind_isEquivalent', 'cetTitleKind_isFederal',
                'cetTitleKind_isAcknowledgement', 'cetTitleType', 'permission_id',
                'permission_parentId', 'permission_isActive', 'permission_textDe', 'permission_textFr',
                'permission_textIt', 'permission_textEn', 'permission_isNada', 'permission_isBgmd',
                'permission_isEquivalent', 'permission_isFederal', 'permission_isAcknowledgement']
df = df[column_order]

# save full records to file
df.to_csv('data/psyreg_full.csv', index=False)

# get subset of id, name and permission columns
column_order_permissions = ['id', 'name', 'firstName', 'link', 'permission_id',
                'permission_parentId', 'permission_isActive', 'permission_textDe', 'permission_textFr',
                'permission_textIt', 'permission_textEn', 'permission_isNada', 'permission_isBgmd',
                'permission_isEquivalent', 'permission_isFederal', 'permission_isAcknowledgement']
df_permissions = df[column_order_permissions]

# drop duplicates
df_permissions.drop_duplicates(subset=['id'], inplace=True)

# save to file
df_permissions.to_csv('data/psyreg.csv', index=False)
