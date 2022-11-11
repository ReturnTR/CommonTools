
# 开始时间，结束时间，运行用时

# 使用方法：在run.sh目录下执行 bash run.sh test.py &

# 功能：1.程序计时  2.自动在程序所在目录下创建log文件



start_time=`date +'%Y-%m-%d %H:%M:%S'`

python -u $1 > $1".log" 2>&1  # 将错误信息视为标准信息

end_time=`date +'%Y-%m-%d %H:%M:%S'`



start_seconds=$(date --date="$start_time" +%s)
end_seconds=$(date --date="$end_time" +%s)
eclipsed_seconds=$((end_seconds-start_seconds))
second=$(($eclipsed_seconds % 60))
min=$(($eclipsed_seconds % 3600 /60 ))
hour=$(($eclipsed_seconds / 3600))

echo "-------------------用时------------------" >> $1".log" 
echo "开始时间："$start_time >> $1".log" 
echo "结束时间："$end_time >> $1".log" 
echo "用时："$hour"h "$min"m "$second"s" >> $1".log"

