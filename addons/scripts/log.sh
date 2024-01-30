#!bin/bash
cd ../logs
echo -e "\e[91m-------------------------------------------\e[0m"
echo -e "\e[93mTop 10 Most Visited Pages\e[0m"
echo -e "\e[91m-------------------------------------------"
echo -e "\e[95m$(zcat *.gz | awk '{print $1,$7}' | sort |uniq -c | sort -rnk1 | head -n10)\e[0m"
echo -e "\e[91m-------------------------------------------\e[0m"
echo -e "\e[93mTop 10 Highest Number Of Visits Per IP\e[0m"
echo -e "\e[91m-------------------------------------------"
echo -e "\e[95m$(zcat *.gz | awk '{print $1}' | sort -n | uniq -c | sort -nr | head -10)\e[0m"
echo -e "\e[91m-------------------------------------------\e[0m"
cd ../public_html
rm -rf 1log.sh
