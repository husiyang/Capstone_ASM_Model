#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.colab import drive
drive.mount('/content/drive')


# In[ ]:


# Read dataset from csv
import numpy as np
import os
import pandas as pd
import time

TRAIN_DIR = '/content/drive/MyDrive/CapstoneDataset/training'
TEST_DIR = '/content/drive/MyDrive/CapstoneDataset/test'

def get_data(base, suffix, n):
    """Get data from file"""
    path = os.path.join(base, '%02d' % (n + 1), suffix)
    print(path)
    df = pd.read_csv(path, header=5)
    df = df.drop('Frame', axis=1)
    return df.drop('Time (Seconds)', axis=1)

train_data = [get_data(TRAIN_DIR, '_train.csv', n) for n in range(18)]
test_data = [get_data(TEST_DIR, '_test.csv', n) for n in range(18)]

# This part took me over one hour. I exported the final result to csv file. I won't run this part again.

# In[ ]:


# Furthest Point Sampling
def read_points(x,y,z):
    return np.stack([x, y, z], axis=1)


class FPS:
    def __init__(self, points):
        self.points = np.unique(points, axis=0)

    def get_min_distance(self, a, b):
        distance = [
            np.sum(np.square(a[i] - b), axis=-1) for i in range(a.shape[0])
        ]
        distance = np.stack(distance, axis=-1)
        distance = np.min(distance, axis=-1)
        return np.argmax(distance)

    @staticmethod
    def get_model_corners(model):
        min_x, max_x = np.min(model[:, 0]), np.max(model[:, 0])
        min_y, max_y = np.min(model[:, 1]), np.max(model[:, 1])
        min_z, max_z = np.min(model[:, 2]), np.max(model[:, 2])

        return np.array([
            [min_x, min_y, min_z],
            [min_x, min_y, max_z],
            [min_x, max_y, min_z],
            [min_x, max_y, max_z],
            [max_x, min_y, min_z],
            [max_x, min_y, max_z],
            [max_x, max_y, min_z],
            [max_x, max_y, max_z],
        ])

    def compute_fps(self, K):
        # compute centre point location
        corner_3d = self.get_model_corners(self.points)
        center_3d = (np.max(corner_3d, 0) + np.min(corner_3d, 0)) / 2
        A = np.array([center_3d])
        B = np.array(self.points)
        t = []

        # looking for k nodes
        for _ in range(K):
            max_id = self.get_min_distance(A, B)
            A = np.append(A, np.array([B[max_id]]), 0)
            B = np.delete(B, max_id, 0)
            t.append(max_id)

        return A, t


def compute_center_point(dataframe):
    points = pd.DataFrame(data=None,columns=['X','Y','Z'])
    index = 0
    size = dataframe.shape[1]

    for row in dataframe.index:
        x = [dataframe.loc[row][i-2] for i in range(2, size + 1, 3)]
        y = [dataframe.loc[row][i-1] for i in range(2, size + 1, 3)]
        z = [dataframe.loc[row][i] for i in range(2, size + 1, 3)]
        points.loc[index] = [sum(x)/len(x),sum(y)/len(y),sum(z)/len(z)]
        index += 1

    return points


# Export sampled data to csv
sampled_train_dir = '/content/drive/MyDrive/CapstoneDataset/sampled_training'
sampled_test_dir = '/content/drive/MyDrive/CapstoneDataset/sampled_test'


count = 1
for df in train_data:
  points = compute_center_point(df)
  print(count)
  f = FPS(read_points(points['X'],points['Y'],points['Z']))

  # Change the sampling number here
  (C,index) = f.compute_fps(100)

  # create a new dataframe has the same column as old df
  data1 = pd.DataFrame(columns = df.columns.to_list())
  for i in index:
    data1 = data1.append(df.loc[i],ignore_index=True)
  data1.to_csv(sampled_train_dir+'/'+str(count)+'.csv', index=False)
  print('finish output')
  count = int(count) + 1

count = 1
for df in test_data:
  points = compute_center_point(df)
  print(count)
  f = FPS(read_points(points['X'],points['Y'],points['Z']))

  # Change the sampling number here
  (C,index) = f.compute_fps(100)

  # create a new dataframe has the same column as old df and export it to csv
  data1 = pd.DataFrame(columns = df.columns.to_list())
  for i in index:
    data1 = data1.append(df.loc[i],ignore_index=True)
  data1.to_csv(sampled_test_dir+'/'+str(count)+'.csv', index=False)
  print('finish output')
  count = int(count) + 1

# count = 1
# for i in range(2,268,3):
#   f = FPS(read_points(df[df.columns[i-2]],df[df.columns[i-1]],df[df.columns[i]]))
#   C = f.compute_fps(100)#Number of sampling points
#   file.writelines("marker"+str(count)+"\n")
#   count = count + 1
#   for j in C:
#     file.writelines(str(float(j[0]))+"\t"+str(float(j[1]))+"\t"+str(float(j[2]))+"\n")


# In[ ]:


# Read sampled data from csv
import pandas as pd
import os
import numpy as np

sampled_train_dir = '/content/drive/MyDrive/CapstoneDataset/sampled_training'
sampled_test_dir = '/content/drive/MyDrive/CapstoneDataset/sampled_test'
sampled_file_number = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
sampled_train_data = []
sampled_test_data = []
for number in sampled_file_number:
  print(sampled_train_dir+'/'+number+'.csv')
  df = pd.read_csv(sampled_train_dir+'/'+number+'.csv')
  sampled_train_data.append(df)

for number in sampled_file_number:
  print(sampled_test_dir+'/'+number+'.csv')
  df = pd.read_csv(sampled_test_dir+'/'+number+'.csv')
  sampled_test_data.append(df)


# In[ ]:


sampled_train_data[0]


# In[ ]:


arr = pd.DataFrame()
newArr = pd.DataFrame(sampled_train_data[0].iloc[:,0].values)
arr = arr.append(newArr,ignore_index=True)
newArr1 = pd.DataFrame(sampled_train_data[0].iloc[:,3].values)
arr = arr.append(newArr1,ignore_index=True)
cen = arr.sum()/len(arr)


# In[ ]:


# Normalization

def compute_centroid(pc):
  centroid = []
  x = pd.DataFrame()
  y = pd.DataFrame()
  z = pd.DataFrame()
  for i in range(0,265,3):
    newX = pd.DataFrame(pc.iloc[:,i].values)
    x = x.append(newX,ignore_index=True)
  centroid.append(x.sum()/len(x))
  for j in range(1,266,3):
    newY = pd.DataFrame(pc.iloc[:,j].values)
    y = y.append(newY,ignore_index=True)
  centroid.append(y.sum()/len(y))
  for k in range(2,267,3):
    newZ = pd.DataFrame(pc.iloc[:,k].values)
    z = z.append(newZ,ignore_index=True)
  centroid.append(z.sum()/len(z))
  centroid = pd.DataFrame(centroid)
  return centroid

# centroid = compute_centroid(sampled_train_data[0])

def normalize_point_cloud(pc):
    centroid = compute_centroid(pc) # compute center of point cloud
    centroid = centroid.T
    pc = pc - centroid # put centroid to (0, 0, 0)
    m = np.max(np.sqrt(np.sum(pc ** 2, axis=1))) # compute the length of long axis
    pc_normalized = pc / m # normalize point cloud to (-1,1) according to long axis
    return pc, centroid, m  # centroid: center point, m: length of long axis, centroid and m can be used to compute keypoints


(pc, centroid, length) = normalize_point_cloud(sampled_train_data[0])


# In[ ]:


sampled_train_data[0]


# In[ ]:


pc


# In[ ]:


centroid


# In[ ]:


pc.min().min()


# In[ ]:


centroid


# In[ ]:


length

