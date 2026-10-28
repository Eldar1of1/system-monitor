import speedtest

test = speedtest.Speedtest(secure=True)

test.get_best_server()

ping = test.results.ping

print(ping)