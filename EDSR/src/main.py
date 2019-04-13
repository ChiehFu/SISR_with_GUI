import torch

import utility
import data
import model
import loss as l
from option import args
from trainer import Trainer

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)

def main():
    global model
    torch.cuda.device_count()
    torch.cuda.get_device_name(0)
    if args.data_test == 'video':
        from videotester import VideoTester
        model = model.Model(args, checkpoint)
        t = VideoTester(args, model, checkpoint)
        t.test()
    else:
        if checkpoint.ok:
            loader = data.Data(args)
            model = model.Model(args, checkpoint)
            loss = l.Loss(args, checkpoint) if not args.test_only else None
            t = Trainer(args, loader, model, loss, checkpoint)
            while not t.terminate():
                t.train()
                t.test()

            checkpoint.done()

if __name__ == '__main__':
    main()
