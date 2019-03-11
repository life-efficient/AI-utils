import torch

def getDataLoaders(dataset, batch_size=4, splits=None):

    if splits is None:
        splits = [0.8, 0.15, 0.05]
    assert sum(splits) == 1
    train_size = int(splits[0] * len(dataset))
    val_size = int(splits[1] * len(dataset))
    test_size = len(dataset) - train_size - val_size

    train_data, val_data, test_data = torch.utils.data.random_split(dataset, [train_size, val_size, test_size])

    train_loader = torch.utils.data.DataLoader(train_data, shuffle=True, batch_size=batch_size)
    val_loader = torch.utils.data.DataLoader(val_data, shuffle=True, batch_size=batch_size)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size)

    return train_loader, val_loader, test_loader