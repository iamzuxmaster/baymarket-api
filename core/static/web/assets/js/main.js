

/*=============================================
	=     Menu sticky & Scroll to top      =
=============================================*/
var prevScrollpos = window.pageYOffset;
$(window).on('scroll', function () {
	var scroll = $(window).scrollTop();
	if (scroll > 200) {
	var currentScrollPos = window.pageYOffset;
	if (prevScrollpos > currentScrollPos) {
		$("#navigation").addClass("sticky-menu");
	} else {
		$("#navigation").removeClass("sticky-menu");
	}
	} else {
		$("#navigation").removeClass("sticky-menu");
	}
	prevScrollpos = currentScrollPos;

});


// Category - Carousel
$('.owl-carousel').owlCarousel({
    margin:10,
    nav:true,
	autoplay:true,
    autoplayTimeout:5000,
    autoplayHoverPause:true,
    responsive:{
        0:{
            items:1
        },
		400:{
            items:2
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
})

//Filter Dropown Toggle
// if ($('.filter-accardion li.menu-item-has-children ul').length) {
// 	$('.filter-accardion li.menu-item-has-children').append('<div class="dropdown-btn"><ion-icon name="chevron-down-outline"></ion-icon></div>');

// }

//Mobile Nav Hide Show
// if ($('.filter-accardion').length) {

// 	//Dropdown Button
// 	$('.filter-accardion li.menu-item-has-children .dropdown-btn').on('click', function () {
// 		$(this).toggleClass('open');
// 		$(this).prev('ul').slideToggle(500);
// 	});
// }

//Dropdown Button


$('.navigation li.menu-item-has-children a').on('click', function () {
	$(this).next('ul.submenu').slideToggle(500);
});


/*=============================================
	=    	 Slider Range Active  	         =
=============================================*/
// $("#slider-range").slider({
// 	range: true,
// 	min: 0,
// 	max: 700,
// 	values: [0, 700],
// 	slide: function (event, ui) {
// 		$("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
// 	}
// });
// $("#amount").val("$" + $("#slider-range").slider("values", 0) + " - $" + $("#slider-range").slider("values", 1));

// $("#slider-range2").slider({
// 	range: true,
// 	min: 0,
// 	max: 700,
// 	values: [0, 700],
// 	slide: function (event, ui) {
// 		$("#amount2").val("$" + ui.values[0] + " - $" + ui.values[1]);
// 	}
// });
// $("#amount2").val("$" + $("#slider-range2").slider("values", 0) + " - $" + $("#slider-range2").slider("values", 1));



// Open .Close katalog


let katalog = document.querySelectorAll('#katalog-btn') 
let menu_katalog = document.querySelector('#menu-katalog') 
let page =  document.querySelector("#page")
let logo = document.querySelectorAll("#nav-logo")
katalog.forEach(k => {
	k.addEventListener('click', () => {
		menu_katalog.classList.remove('d-none')
		page.classList.add('d-none')
		page.classList.add('opacity_')
		setTimeout(function() {
			menu_katalog.classList.replace('opacity_', '_opacity')
		}, 100 );
	})
})

logo.forEach(l => {
	l.addEventListener('click', () => {
		menu_katalog.classList.add('d-none')
		page.classList.remove('d-none')
		menu_katalog.classList.replace('_opacity', 'opacity_')
		setTimeout(function() {
			page.classList.replace('opacity_', '_opacity')
        }, 100 );
	})
})


// #################### On Of Butoon ##########################
if (document.querySelectorAll('.on-of-btn')) {
	let change_label = document.querySelectorAll('.on-of-btn')
	let box = document.querySelectorAll('#r-l-box')
	change_label.forEach((ch_b, index) => {
		ch_b.addEventListener('click', () => {
				if(box[index].classList.value.includes('r-box')) {
					box[index].classList.replace('r-box', 'l-box')
				} else {
					box[index].classList.replace('l-box', 'r-box')
				}
		})
	})

}


// ################# Mumber Show And Hide #####################
if(document.querySelector('#number-show-hide')) {
	let number_show_hide = document.querySelector('#number-show-hide')
	let number_show = document.querySelector('#number-show')
	let number_hide = document.querySelector('#number-hide')
	number_show_hide.addEventListener('click', () => {
		if(number_show.classList.value.includes('d-none')) {
			number_show.classList.remove('d-none')
			number_hide.classList.add('d-none')
			number_show_hide.innerText = "Berkitish"
		} else {
			number_show.classList.add('d-none')
			number_hide.classList.remove('d-none')
			number_show_hide.innerText = "Korsatish"
		}
	})
}
