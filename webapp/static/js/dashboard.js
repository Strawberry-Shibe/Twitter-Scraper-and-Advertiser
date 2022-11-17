let countdowns = {};

/**
 * converts a polar coordinate with center point to a cartesian coordinate
 *
 * @authors Matt
 * @param   centerX     {number} center x coordinate
 * @param   centerY     {number} center y coordinate
 * @param   radius      {number} radius
 * @param   angleDeg    {number} angle from the polar axis going anti-clockwise, measured in degrees
 * @return              {{x: number, y: number}}
 */
function polarToCartesian(centerX, centerY, radius, angleDeg) {
	let angleRads = (angleDeg/180) * Math.PI;
	return {
		x: Number(centerX + (radius * Math.cos(angleRads))),
		y: Number(centerY + (radius * Math.sin(angleRads)))
	}
}

/**
 * generates the d attribute for an svg path element described by the input values
 *
 * @authors Matt
 * @param   x           {number} x coordinate for the center of the arc
 * @param   y           {number} y coordinate for the center of the arc
 * @param   radius      {number} radius of the arc
 * @param   startAngle  {number} starting angle of the arc in degrees
 * @param   endAngle    {number} ending angle of the arc in degrees
 * @return              {string}
 */
function describeArc(x, y, radius, startAngle, endAngle) {
	let start = polarToCartesian(x, y, radius, endAngle);
	let end = polarToCartesian(x, y, radius, startAngle);

	let largeArcFlag = Number((endAngle - startAngle >= 180)).toString();
	let sweepFlag = Number((endAngle - startAngle >= 360)).toString();

	return ["M", start.x, start.y, "A", radius, radius, "0", largeArcFlag, sweepFlag, end.x, end.y].join(" ");
}

/**
 * clamps an input value between a maximum and a minimum value
 *
 * @authors Matt
 * @param   val {number} the input value
 * @param   min {number} the minimum output value
 * @param   max {number} the maximum output value
 * @return      {number}
 */
function value_limit(val, min, max) {
	return val < min ? min : (val > max ? max : val);
}

/**
 * function to get all countdowns on the dashboard into a formatted state
 * based on the "static" data from the templater
 *
 * TODO add functionality to start countdowns on page load rather than having to wait for the next websocket message
 *
 * @authors     Matt
 * @returns     {null}
 */
function countdown() {
	let countdowns = document.getElementsByClassName("circular-countdown");
	if (countdowns.length >= 1) {
		for (let countdown of countdowns) {
			let top_id = countdown.getAttribute("id");
			let last_time = new Date(Number(countdown.getAttribute("lasttime")) * 1000);
			let next_time = new Date(Number(countdown.getAttribute("nexttime")) * 1000);
			let interval = next_time - last_time;
			update_countdown(countdown.getElementsByClassName("fg-path")[0],
							countdown.getElementById(top_id.concat("-value")),
							next_time, interval);
		}
	}
}

const socket = io("/dashboard");
socket.on('twitter_scraper_update', function (data) {
	let last_scrape = document.getElementById("last_twitter_scrape_timestamp");
	let countdown_id = "tweet_scrape_cd";
	let countdown = document.getElementById(countdown_id);
	let out_of =  document.getElementById(countdown_id.concat("-out-of"));
	let value =  document.getElementById(countdown_id.concat("-value"));

	let now_time = Date.now();
	let last_time = new Date(Number(data["last_time"]) * 1000);
	let next_time = new Date(Number(data["next_time"]) * 1000);
	let interval = Number(data["interval"]);

	last_scrape.getElementsByClassName("circle-display-value")[0].innerHTML = last_time.toISOString().substr(11, 8);
	out_of.innerHTML = next_time.toISOString().substr(11, 8);
	let scale = countdown.getElementsByClassName("fg-path")[0];

	for (let i = 0; i<interval; i++) {
		setTimeout(update_countdown, 1000*i, scale, value, next_time, interval, i);
	}
});

// const socket = io("/dashboard");
socket.on('data_update', function (data) {
	for (const [key, value] of Object.entries(data)) {
		if (value["type"] === "scale") {
			let text = document.getElementById(key);
			text.innerHTML = value["value"];
			let scale = document.getElementById(key.concat("-circular-scale"));
			scale.setAttribute("d", describeArc(8, 8, 7, 135,135+(270*(value["value"]/value["max"]))))
		} else if (value["type"] === "countdown") {
			clearTimeout(countdowns[key]);
			let now = new Date();

			let last = document.getElementById(value["last"]);
			last.innerHTML = now.toTimeString().substr(0,8);

			now.setTime(now.getTime() + value["length"]*1000);
			let next = document.getElementById(key.concat("-out-of"));
			next.innerHTML = now.toTimeString().substr(0, 8);
			countdown2(key, value["length"], value["length"]);

		} else {
			let text = document.getElementById(key);
			text.innerHTML = value["value"];
		}
	}
});

/**
 * Function that updates a countdown scale and value.
 *
 * @author  Matt
 * @param   scale     {element}   svg path element, the foreground path (fg-path) of the scale
 * @param   value     {element}   svg text element, displays the current value of the scale
 * @param   next_time {Date}      Date object with the end time for the countdown
 * @param   interval  {number}    Total length of the countdown, start to end, in seconds
 * @returns           {null}
 */
function update_countdown(scale, value, next_time, interval) {
	let diff = next_time - Date.now();
	let output;
	if (Math.floor(diff/3600000) !== 0) {
		output = new Date(diff).toISOString().substr(11, 8);
	} else {
		output = new Date(diff).toISOString().substr(14, 5);
	}
	value.innerHTML = output;
	value.setAttribute('font-size', font_size_calc(output));
	let endAngle = 405-(value_limit((diff/(interval*1000)), 0, 1))*270;
	scale.setAttribute("d", describeArc(8,8,7, 135, endAngle));

	return null;
}

/**
 * calculates font size for text within svg circle using the length of input string
 *
 * @author  Matt
 * @param   input   {string}    String input of which to calculate the font size for.
 * @return          {string}    String output with the fontsize percentage.
 */
function font_size_calc(input) {
	let string_length = input.length;
	// let decimal = 1.24194 - 0.231619*Math.log((15.2666*string_length)-6.20299); // old approximation
	// new approximation
	let decimal = 0.04889127+0.42963403/(1+(string_length/3.496243)**3.158169)**0.518323;
	let percent = (decimal*100).toFixed(2);
	return String(percent).concat("%");
}

function countdown2(ele, prev, max) {
	prev = Math.floor(prev);
	let text = document.getElementById(ele.concat("-value"));
	let disp = new Date(prev * 1000).toISOString().substr(11, 8);
	text.innerHTML = disp;

	let curve = document.getElementById(ele.concat("-curve"))
	curve.setAttribute("d", describeArc(8, 8, 7, 135, 135+(270*(prev/max))));

	if (prev !== 0){
		prev--;
		countdowns[ele] = setTimeout(countdown2, 1000, ele, prev, max)
	}
}