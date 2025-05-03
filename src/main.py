from invoice import Invoice

def main():
    inv = Invoice("test2.pdf")
    inv.parse()
    print(inv)

if __name__ == "__main__":
    main()