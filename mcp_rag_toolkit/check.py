import pickle

with open("index/doc_mapping.pkl", "rb") as f:
    mapping = pickle.load(f)

print(type(mapping))        # Should be dict
print(list(mapping.items()))  # Should show index: path mappings