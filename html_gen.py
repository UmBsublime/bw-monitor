#!/usr/bin/env python

LOG_PATH = '/home/cvaillancourt/log/bwmd.py.log'

template_top = '''<!doctype html>
<html>
	<head>
		<title>Line Chart</title>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.js"></script>
	</head>
	<body>
		<div style="width:30%">
			<div>
				<canvas id="canvas" height="650" width="1200"></canvas>
			</div>
		</div>


	<script>
		var randomScalingFactor = function(){ return Math.round(Math.random()*100)};
		var lineChartData = {
			labels :  '''
template_time = '{}'

template_mid = ''',
			datasets : [
				{
					label: "My First dataset",
					fillColor : "rgba(220,220,220,0.2)",
					strokeColor : "rgba(220,220,220,1)",
					pointColor : "rgba(220,220,220,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(220,220,220,1)",
					data :  '''

template_value = '{}'

template_bot = '''
				},
				{
					label: "My Second dataset",
					fillColor : "rgba(151,187,205,0.2)",
					strokeColor : "rgba(151,187,205,1)",
					pointColor : "rgba(151,187,205,1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : "rgba(151,187,205,1)",
					data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
				}
			]
		}
	window.onload = function(){
		var ctx = document.getElementById("canvas").getContext("2d");
		window.myLine = new Chart(ctx).Line(lineChartData, {
			responsive: true
		});
	}
	</script>
	</body>
</html>
'''


def convert_to_deltas(value_list):

    if len(value_list) >= 2:
        temp = value_list[0]
        value_list = value_list[1:]
        deltas =[]
        for v in value_list:
            t = int(v) - int(temp)
            deltas.append(str(t))
            temp =v

        return deltas


with open(LOG_PATH) as log:
    content = log.readlines()

values = []
times = []
for line in content:
    if "HTTP out a" in line:
        temp = line.split(' ')
        time = temp[:2]
        time = ' '.join(time)
        time = time.replace('[', ' ')
        time = time.replace(']', ' ')
        time = time.split(' ')
        #time = ' '.join(time[1:3])
        time = time[2]
        time = time.split(',')[0]

        value = temp[-1]
        value = value.replace('\n', '')
        times.append(time)
        values.append(value)


times = times[1:]
values = convert_to_deltas(values)

if len(times) >= 20:
    times = times[-20:]
    values = values[-20:]

print template_top + repr(times) + template_mid + repr(values) + template_bot

#print convert_to_deltas(values)
