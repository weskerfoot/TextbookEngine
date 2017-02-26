#! /usr/bin/bash

while inotifywait -qqre modify "./src"; do
  fab buildLocal
done
