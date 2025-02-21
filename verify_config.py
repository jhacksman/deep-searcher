from deepsearcher.configuration import Configuration, init_config

def main():
    config = Configuration()
    init_config(config)
    print('Configuration initialized successfully')

if __name__ == '__main__':
    main()
