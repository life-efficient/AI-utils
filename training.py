import matplotlib.pyplot as plt
from profiler import Timer

def train(model, dataloader, criterion, optimiser, epoch, figure, axis, train_losses, timer):
    for batch_idx, batch in enumerate(dataloader):
        x, y = batch
        timer.start('forward pass')
        prediction = model(x)
        timer.stop('forward pass')
        #print('Input shape:', x.shape)
        #print('Prediction shape:', prediction.shape)
        loss = criterion(prediction, y)
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
        print('Epoch:', epoch, '\tBatch:', batch_idx, '\tLoss:', loss.item())
        train_losses.append(loss.item())
        axis.plot(train_losses, 'b')
        figure.canvas.draw()

        if batch_idx == 10:
            #break
            pass

def evaluate(model, dataloader, criterion, epoch, figure, axis, val_losses):
    model.eval()
    for batch_idx, batch in enumerate(dataloader):
        x, y = batch
        prediction = model(x)
        loss = criterion(prediction, y)
        print('Epoch:', epoch, '\tBatch:', batch_idx, '\tLoss:', loss.item())
        val_losses.append(loss.item())
        axis.plot(val_losses, 'g')
        figure.canvas.draw()
    model.train()

def getLossPlot():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('Batch')
    plt.ylabel('Loss')
    plt.ion()
    plt.show()
    return fig, ax
