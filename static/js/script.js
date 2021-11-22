jQuery(function ($) {
	'use strict';

	/* ----------------------------------------------------------- */
	/*  Fixed header
	/* ----------------------------------------------------------- */
	$(window).on('scroll', function () {

		// fixedHeader on scroll
		function fixedHeader() {
			var headerTopBar = $('.top-bar').outerHeight();
			var headerOneTopSpace = $('.header-one .logo-area').outerHeight();

			var headerOneELement = $('.header-one .site-navigation');
			var headerTwoELement = $('.header-two .site-navigation');

			if ($(window).scrollTop() > headerTopBar + headerOneTopSpace) {
				$(headerOneELement).addClass('navbar-fixed');
				$('.header-one').css('margin-bottom', headerOneELement.outerHeight());
			} else {
				$(headerOneELement).removeClass('navbar-fixed');
				$('.header-one').css('margin-bottom', 0);
			}
			if ($(window).scrollTop() > headerTopBar) {
				$(headerTwoELement).addClass('navbar-fixed');
				$('.header-two').css('margin-bottom', headerTwoELement.outerHeight());
			} else {
				$(headerTwoELement).removeClass('navbar-fixed');
				$('.header-two').css('margin-bottom', 0);
			}
		}
		fixedHeader();


		// scroll to top btn show/hide
		function scrollTopBtn() {
			var scrollToTop = $('#back-to-top'),
				scroll = $(window).scrollTop();
			if (scroll >= 50) {
				scrollToTop.fadeIn();
			} else {
				scrollToTop.fadeOut();
			}
		}
		scrollTopBtn();
	});


	const state = {
		storagePrice: 0,
		boxSizePrice: 0,
		rentTime: 1
	}

	const yearPriceSpan = document.querySelector("#price-per-year")
	const storageAddressSelect = document.querySelector("#address")
	const boxSizeSelect = document.querySelector("#box-size")
	const rentTimeSelect = document.querySelector("#rent-term")

	function countPrice(){
		let price = 0
		price += state.storagePrice
		price += state.boxSizePrice
		price *= state.rentTime
		return price
	}

	function changePrice() {
		yearPriceSpan.innerHTML = `${countPrice()}`
	}

	function changePricesCallback(event) {
		if (event.target === storageAddressSelect) {
			state.storagePrice = parseFloat(event.target.options[event.target.selectedIndex].getAttribute('data-price'))
		} else if (event.target === boxSizeSelect) {
			state.boxSizePrice = parseFloat(event.target.options[event.target.selectedIndex].getAttribute('data-price'))
		} else if (event.target === rentTimeSelect) {
			state.rentTime = parseInt(event.target.value)
		} else {}
		changePrice()
	}

	storageAddressSelect.addEventListener("change", (event) => changePricesCallback(event), false)

	boxSizeSelect.addEventListener("change", (event) => changePricesCallback(event), false)

	rentTimeSelect.addEventListener("change", (event) => changePricesCallback(event), false)

	function initChangePrices() {
		state.boxSizePrice = parseFloat(boxSizeSelect.options[boxSizeSelect.selectedIndex].getAttribute('data-price'))
		state.storagePrice = parseFloat(storageAddressSelect.options[boxSizeSelect.selectedIndex].getAttribute('data-price'))
		state.rentTime = parseInt(rentTimeSelect.value)

		changePrice()
	}

	initChangePrices()
});