from fake_headers import Headers

if __name__ == "__main__":
    header = Headers(
        # generate any browser & os headeers
        browser="chrome",
        headers=True  # don`t generate misc headers
    )

    for i in range(30):
        print(header.generate(), ",")
