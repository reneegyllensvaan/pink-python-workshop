from completed import channel, exchange_name, queue_name, listen

print('Listening on <' + exchange_name + '>, queue name ' + queue_name)

listen(channel)
