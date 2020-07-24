


pre_rx_time=time.perf_counter()
post_rx_time=time.perf_counter()
print("rx delay: ", post_rx_time-pre_rx_time)
pre_tx_time=time.perf_counter()
print("process delay: ", pre_tx_time-post_rx_time)
post_tx_time=time.perf_counter()
print("tx delay: ", post_tx_time-pre_tx_time)