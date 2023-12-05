import boto3
from tqdm import tqdm

s3 = boto3.client('s3')

bucket_name = 'snapshots-ml'

keys = []
for prefix in ['knockout/image_data/screen/inputs/']:
    paginator = s3.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix
    )
    for page in response_iterator:
        for obj in page['Contents']:
            key = obj['Key']
            keys.append(key)
for key in tqdm(keys[:10000]):
    file_name = key.split("/")[-1]
    if len(file_name) == 0:
        continue
    s3.download_file(bucket_name,
                     key,
                     f'/home/ubuntu/train_data/inputs/{file_name}'
                     )
for file in tqdm(os.listdir(f'/home/ubuntu/train_data/inputs/')):
    file_name = os.fsdecode(file)
    if len(file_name) == 0:
        continue
    key = f'knockout/image_data/screen/ground_truth/{file_name[:-3]}PNG'
    s3.download_file(bucket_name,
                     key,
                     f'/home/ubuntu/train_data/ground_truth/{file_name[:-3]}PNG'
                     )

