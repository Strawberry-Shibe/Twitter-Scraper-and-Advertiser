/**
 * function to collapse and expand the side navbar by changing some css variables
 *
 * @author  Matt
 */
function collapse() {
	let root = document.documentElement;
	if (root.style.getPropertyValue('--collapse') === "inline") {
		root.style.setProperty('--collapse', "none");
		root.style.setProperty('--collapse-inv', "inline");
		root.style.setProperty('--text-width', "0");
		root.style.setProperty('--text-width-inv', "1");
		root.style.setProperty('--icon-rotate', "180deg");
		root.style.setProperty('--icon-align', "center");
		root.style.setProperty('--width', "4vw");
		root.style.setProperty('--icon-scale', "1.3");
		root.style.setProperty('--a-width', "4vw");
		root.style.setProperty('--icon-width', "2vw");
		root.style.setProperty('--logo-height', "calc(var(--width)/0.75)");

	} else {
		root.style.setProperty('--collapse', "inline");
		root.style.setProperty('--collapse-inv', "none");
		root.style.setProperty('--text-width', "1");
		root.style.setProperty('--text-width-inv', "0");
		root.style.setProperty('--icon-rotate', "0deg");
		root.style.setProperty('--icon-align', "left");
		root.style.setProperty('--width', "20vw");
		root.style.setProperty('--icon-scale', "1");
		root.style.setProperty('--a-width', "100%");
		root.style.setProperty('--icon-width', "30px");
		root.style.setProperty('--logo-height', "calc(var(--width)/5)");
	}
}

/**
 * function to control the dropdown nav menu on portrait devices
 *
 * @author  Matt
 */
function dropdown() {
	let root = document.documentElement;
	let icon = document.getElementById("menu-icon");
	let dropList = document.getElementById("dropLinks");
	if (root.style.getPropertyValue('--dropdown') === "0") {
		root.style.setProperty('--dropdown', "100vh");
		root.style.setProperty('--dropdown-content-height', "12vw");
		root.style.setProperty('--dropdown-content-overflow', "hidden");
		root.style.setProperty('--dropdown-content-margin', "0");

		icon.classList.toggle('expanded')
		icon.classList.toggle('collapsed')

		dropList.classList.toggle('dropHidden')
	} else {
		root.style.setProperty('--dropdown', "0");
		root.style.setProperty('--dropdown-content-height', "100%");
		setTimeout(() => { root.style.setProperty('--dropdown-content-overflow', "visible"); }, 500);
		root.style.setProperty('--dropdown-content-margin', "12vw");

		icon.classList.toggle('expanded')
		icon.classList.toggle('collapsed')

		dropList.classList.toggle('dropHidden')
	}
}

collapse();
dropdown();
