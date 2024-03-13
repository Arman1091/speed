
var perimetre = 0;
var long = 0;
var larg = 0;
var surface = 0;
(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  // let navbarlinks = select('#navbar .scrollto', true)
  // const navbarlinksActive = () => {
  //   let position = window.scrollY + 200
  //   navbarlinks.forEach(navbarlink => {
  //     if (!navbarlink.hash) return
  //     let section = select(navbarlink.hash)
  //     if (!section) return
  //     if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
  //       navbarlink.classList.add('active')
  //     } else {
  //       navbarlink.classList.remove('active')
  //     }
  //   })
  // }
  // window.addEventListener('load', navbarlinksActive)
  // onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  // const scrollto = (el) => {
  //   let header = select('#header')
  //   let offset = header.offsetHeight

  //   let elementPos = select(el).offsetTop
  //   window.scrollTo({
  //     top: elementPos - offset,
  //     behavior: 'smooth'
  //   })
  // }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  // let selectHeader = select('#header')
  // let selectTopbar = select('#topbar')
  // if (selectHeader) {
  //   const headerScrolled = () => {
  //     if (window.scrollY > 100) {
  //       selectHeader.classList.add('header-scrolled')
  //       if (selectTopbar) {
  //         selectTopbar.classList.add('topbar-scrolled')
  //       }
  //     } else {
  //       selectHeader.classList.remove('header-scrolled')
  //       if (selectTopbar) {
  //         selectTopbar.classList.remove('topbar-scrolled')
  //       }
  //     }
  //   }
  //   window.addEventListener('load', headerScrolled)
  //   onscroll(document, headerScrolled)
  // }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')

  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function (e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function (e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)


  window.addEventListener('load', () => {
    $(".prix_ttc_value").each(function (index, element) {
      let value = parseFloat($(element).text()).toFixed(2);
      $(element).html(value);

    });
    $(".prix_ht_value").each(function (index, element) {
      let value = parseFloat($(element).text()).toFixed(2);
      $(element).html(value);

    });
    $('#dismiss').on('click', function () {
      $('#sidebar').removeClass('active');

    });

    $('#sidebarCollapse').on('click', function () {
      $('#sidebar').addClass('active');

      $('.collapse.in').toggleClass('in');
      $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {

    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });
  // *********counter******************


  const incrementButton = document.getElementById('increment');
  const decrementButton = document.getElementById('decrement');
  const incrementButtonsPlaque = document.getElementsByClassName("increment_plaque");
  const decrementButtonsPlaque = document.getElementsByClassName("decrement_plaque");

  function incrementCounter() {
    const counterElement = document.getElementById('qte');
    let count = counterElement.value;
    count++;
    counterElement.value = count;
    let verif_file = document.getElementById("fileInput").value;
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      console.log(parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht));
      document.getElementById("prix_lin_ht").innerHTML = (count * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht))).toFixed(2);
      document.getElementById("prix_lin_ttc").innerHTML = (count * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc))).toFixed(2);
      document.getElementById("qte_structure").innerHTML = count;
    }
  }
  function incrementPlaque() {
    const counterElement = document.getElementById('qte_plaque');
    let count = counterElement.value;
    count++;
    counterElement.value = count;
  }

  function decrementCounter() {
    const counterElement = document.getElementById('qte');
    let count = counterElement.value;
    if (count > 1) {
      count--;
      counterElement.value = count;
    }
    let verif_file = document.getElementById("fileInput").value;
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      console.log("sd")
      console.log(parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht));
      document.getElementById("prix_lin_ht").innerHTML =(count * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht))).toFixed(2);;
      document.getElementById("prix_lin_ttc").innerHTML = (count * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc))).toFixed(2);;
      document.getElementById("qte_structure").innerHTML = count;
    }
  }
  function decrementPlaque() {

    const counterElement = document.getElementById('qte_plaque');
    let count = counterElement.value;
    if (count > 1) {
      count--;
      counterElement.value = count;
    }
  }
  if (incrementButton && decrementButton) {
    incrementButton.addEventListener('click', incrementCounter);
    decrementButton.addEventListener('click', decrementCounter);
  }

  if (incrementButtonsPlaque && decrementButtonsPlaque) {
    for (let i = 0; i < incrementButtonsPlaque.length; i++) {
      let currentElement = incrementButtonsPlaque[i];
      // var elementBefore = currentElement.previousElementSibling;
      // Perform some action on each element (e.g., change its style)
      if (currentElement) {
        currentElement.addEventListener('click', incrementPlaque);
      }
    }
    for (let i = 0; i < decrementButtonsPlaque.length; i++) {
      let currentElement = decrementButtonsPlaque[i];

      // Perform some action on each element (e.g., change its style)
      if (currentElement) {
        currentElement.addEventListener('click', decrementPlaque);
      }
    }

  }


  // ************** changement epaisseur
  $("#epp").on('change', function () {
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");

    let verif_file = document.getElementById("fileInput").value;
    let formData = new FormData();
    if (verif_file) {
      let file = $('#fileInput')[0].files[0];
      console.log(file);
      formData.append('file', file);
    }

    // console.log(verif_file);

    formData.append('matiere_id', selectedMatiereValue);
    formData.append('type_id', selectedTypeValue);
    formData.append('epaisseur_id', selectedEpaisseurValue);

    $.ajax({
      url: '/change_epaisseur',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        const length_usg = data["types_usinage"].length;
        console.log("sdsds")
        console.log(length_usg)
        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }
        if (data['prix']) {
          var qte = document.getElementById("qte").value;
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(perimetre);
          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
          let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
        }
      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });

  })

  //changement type usinage
  $("#type_usinage").on('change', function () {

    let verif_file = document.getElementById("fileInput").value;

    if (verif_file) {
      let formData = new FormData();
      var selectMatiereElement = document.getElementById("matiere_select");
      var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
      var selectedMatiereValue = selectedMatiereOption.value;

      var selectTypeElement = document.getElementById("type_matiere");
      var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
      var selectedTypeValue = selectedTypeOption.value;

      var selectEpaisseurElement = document.getElementById("epp");
      var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
      var selectedEpaisseurValue = selectedEpaisseurOption.value;

      var selectTypeUsinageElement = document.getElementById("type_usinage");
      var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
      var selectedTypeUsinageValue = selectedTypeUsinageOption.value;
      let file = $('#fileInput')[0].files[0];

      formData.append('file', file);

      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      formData.append('epaisseur_id', selectedEpaisseurValue);
      formData.append('type_usinage_id', selectedTypeUsinageValue);

      $.ajax({
        url: '/change_type_usinage',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          var qte = document.getElementById("qte").value;
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(perimetre);
          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
          let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);

        },
        error: function () {
          alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
        }
      });
    }




  })

  function filterTableRows() {
    var searchText = $('#searche_commande_terminé ').val().toLowerCase();
    console.log(searchText);
    // Iterate through each row in the table body
    $('#historique_table tbody tr').each(function () {
      var currentRow = $(this);
      var tdValues = [];
      currentRow.find('td').each(function () {
        tdValues.push($(this).text());
      });
      var comercials = tdValues[1];
      var clients = tdValues[0];
      // Check if any cell in the row contains the search text

      if (comercials.toLowerCase().indexOf(searchText) === -1 && clients.toLowerCase().indexOf(searchText) === -1) {

        // Hide the row if the search text is not found

        currentRow.hide();

      } else {

        // Show the row if the search text is found

        currentRow.show();

      }
    });
  }

  // Event listener for the input field to trigger filtering on input change
  $('#searche_commande_terminé').keyup(function () {

    filterTableRows();
  });

  function filterTableUsiné() {
    var searchText = $('#search_usiné').val().toLowerCase();
    console.log(searchText);
    // Iterate through each row in the table body
    $('#table_usiné').each(function () {
      var currentRow = $(this);
      var tdValues = [];
      currentRow.find('td').each(function () {
        tdValues.push($(this).text());
      });
      var comercials = tdValues[1];
      var clients = tdValues[0];
      // Check if any cell in the row contains the search text

      if (comercials.toLowerCase().indexOf(searchText) === -1 && clients.toLowerCase().indexOf(searchText) === -1) {

        // Hide the row if the search text is not found

        currentRow.hide();

      } else {

        // Show the row if the search text is found

        currentRow.show();

      }
    });
  }

  // Event listener for the input field to trigger filtering on input change
  $('#search_usiné').keyup(function () {

    filterTableUsiné();
  });

  function filterTableAttents() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('search_en_attants');
    filter = input.value.toLowerCase();
    ul = document.getElementById('en_attents_list');
    li = ul.getElementsByTagName('li');
    var elements = document.querySelectorAll('.contact_name');
    elements.forEach(function(element) {
      
      let text = element.innerText;
      let current_li = element.closest('li');
      console.log(text.toLowerCase());
      if (text.toLowerCase().indexOf(filter) === -1 ) {

        // Hide the row if the search text is not found

        current_li.style.display = 'none';

      } else {
     
        // Show the row if the search text is found

        current_li.style.display = 'block';

      }
    });
    // });
    // var Values = [];
    // for (i = 0; i < li.length; i++) {
    //   Values.push(li[i].innerText);
    //   console.log(Values[i]);
      // txtValue = a.textContent || a.innerText;

      // if (txtValue.toUpperCase().indexOf(filter) > -1) {
      //   li[i].style.display = '';
      // } else {
      //   li[i].style.display = 'none';
      // }
    }
  

  // Event listener for the input field to trigger filtering on input change
  $('#search_en_attants').keyup(function () {

    filterTableAttents();
  });
  $('#text_input').keyup(function () {
    var selectFontElement = document.getElementById("fontSelect");
    var selectedFontOption = selectFontElement.options[selectFontElement.selectedIndex];
    var selectedFontValue = selectedFontOption.value;
    console.log(selectedFontValue);
    var input = document.getElementById('text_input');
    var text = input.value;
    console.log(text);
    console.log(selectedFontValue);
    
    var myTextElement = document.getElementById("visualisation_div");
    myTextElement.style.fontFamily = selectedFontValue; // Replace with your desired font

    // You can also set other font properties like size and color
    myTextElement.style.fontSize = "30px";
    // myTextElement.style.color = "blue";
    myTextElement.innerText=text;
  });
  //   $('#multiple-select').mobiscroll().select({

  //     inputElement: document.getElementById('my-input'),
  //     touchUi: false
  // });
  // **************
  $("#type_matiere").on('change', function () {
    let verif_file = document.getElementById("fileInput").value;
    let formData = new FormData();
    if (verif_file) {
      let file = $('#fileInput')[0].files[0];
      console.log(file);
      formData.append('file', file);
    }
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");
    // var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    // var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

    formData.append('matiere_id', selectedMatiereValue);
    formData.append('type_id', selectedTypeValue);
    $.ajax({
      url: '/change_type',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data["epaisseurs"][0].value)
        while (selectEpaisseurElement.options.length > 0) {
          selectEpaisseurElement.remove(0);
        }
        const length_arr = data["epaisseurs"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["epaisseurs"][i].id;
          newOption.text = data["epaisseurs"][i].value;
          selectEpaisseurElement.add(newOption);
        }

        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usg = data["types_usinage"].length;
        console.log(length_usg)
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }
        if (data['prix']) {
          var qte = document.getElementById("qte").value;
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(perimetre);
          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
          let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
        }
        // let verif_file = $("#fileInput")[0].value;
        // if (verif_file) {
        //   // console.log(verif_file);

        //   var mt = document.getElementById("mt").innerText;
        //   var mt_name = document.getElementById("mt_name").innerText;
        //   formData.append('mt', mt);
        //   formData.append('mt_name', mt_name);
        //   formData.append('selectedValue', selectedValue);
        //   $.ajax({
        //     url: '/change_epaisseur',
        //     type: 'POST',
        //     data: formData,
        //     contentType: false,
        //     processData: false,
        //     success: function (data) {
        //       let prix_decoup_mtr = data['prix'][0][0];
        //       let prix_matiere_mtr = data['prix'][0][1];
        //       // console.log(perimetre);
        //       let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
        //       let formattedNumber_decoup = prix_decoup;
        //       let prix_decoup_ttc = formattedNumber_decoup * 1.2;
        //       let prix_matiere_ht = prix_matiere_mtr * surface;
        //       let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
        //       let total_prix_decoup = prix_matiere_ht + formattedNumber_decoup;
        //       let total_prix_matiere = prix_decoup_ttc + prix_matiere_ttc;
        //       // console.log(total_prix_decoup);
        //       document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
        //       document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
        //       document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
        //       document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
        //       document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
        //       document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


        //       // Change the image source
        //       //  imageElement.src =  'static/img/upload/current.png';
        //       //  let myDiv = document.getElementById("accordionExample");
        //       //  myDiv.style.display = "block";
        //       // let myDiv2 = document.getElementById("prix_total");
        //       // myDiv2.style.display = "block";

        //     },
        //     error: function () {
        //       alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
        //     }
        //   });
        // }
        // let prix_decoup_mtr = data['prix'][0][0];
        // let prix_matiere_mtr = data['prix'][0][1];
        // // console.log(perimetre);
        // let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
        // let formattedNumber_decoup = prix_decoup;
        // let prix_decoup_ttc = formattedNumber_decoup * 1.2;
        // let prix_matiere_ht = prix_matiere_mtr * surface;
        // let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
        // let total_prix_decoup = prix_matiere_ht + formattedNumber_decoup;
        // let total_prix_matiere = prix_decoup_ttc + prix_matiere_ttc;
        // // console.log(total_prix_decoup);
        // document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
        // document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
        // document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
        // document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
        // document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
        // document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });



  });
  // changement matiere
  // **************
  $("#matiere_select").on('change', function () {

    let verif_file = document.getElementById("fileInput").value;
    let formData = new FormData();
    if (verif_file) {
      let file = $('#fileInput')[0].files[0];
      formData.append('file', file);
    }
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;

    var selectTypeElement = document.getElementById("type_matiere");

    var selectEpaisseurElement = document.getElementById("epp");


    var selectTypeUsinageElement = document.getElementById("type_usinage");
    // var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    // var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

    formData.append('matiere_id', selectedMatiereValue);
    // formData.append('type_id', selectedTypeValue);



    // let verif_file = files[0];

    $.ajax({
      url: '/change_matiere',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        if (data['prix']) {
          alert("sdsd");
        }
        while (selectTypeElement.options.length > 0) {
          selectTypeElement.remove(0);
        }
        const length_matieres_types = data["matieres_types"].length;

        for (let i = 0; i < length_matieres_types; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["matieres_types"][i].id;
          newOption.text = data["matieres_types"][i].name;
          selectTypeElement.add(newOption);
        }
        while (selectEpaisseurElement.options.length > 0) {
          selectEpaisseurElement.remove(0);
        }


        const length_arr = data["epaisseurs"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["epaisseurs"][i].id;
          newOption.text = data["epaisseurs"][i].value;
          selectEpaisseurElement.add(newOption);
        }

        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usg = data["types_usinage"].length;
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }


        //       let prix_decoup_mtr = data['prix'][0][0];
        //       let prix_matiere_mtr = data['prix'][0][1];
        //       // console.log(perimetre);
        //       let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
        //       let formattedNumber_decoup = prix_decoup;
        //       let prix_decoup_ttc = formattedNumber_decoup * 1.2;
        //       let prix_matiere_ht = prix_matiere_mtr * surface;
        //       let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
        //       let total_prix_decoup = prix_matiere_ht + formattedNumber_decoup;
        //       let total_prix_matiere = prix_decoup_ttc + prix_matiere_ttc;
        //       // console.log(total_prix_decoup);
        //       document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
        //       document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
        //       document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
        //       document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
        //       document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
        //       document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


        //       // Change the image source
        //       //  imageElement.src =  'static/img/upload/current.png';
        //       //  let myDiv = document.getElementById("accordionExample");
        //       //  myDiv.style.display = "block";
        //       // let myDiv2 = document.getElementById("prix_total");
        //       // myDiv2.style.display = "block";

        if (data['prix']) {
          var qte = document.getElementById("qte").value;
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(perimetre);
          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
          let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
        }

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });



  });

  $(document).ready(function () {

     var fontSelect = document.getElementById("fontSelect");
     var options = fontSelect.getElementsByTagName("option");
     for (var i = 0; i < options.length; i++) {
       console.log(options[i]);
       options[i].style.fontFamily = options[i].value;
     }
    $("#mySelect").change(function () {
      updateSelectedOptions();
    });

    // Update the selected options text
    function updateSelectedOptions() {
      var selectedOptions = $("#mySelect").val();
      console.log(selectedOptions); // You can use the selectedOptions array as needed
    }
    let dropArea = $("#drop-area");

    dropArea.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
      e.preventDefault();
      e.stopPropagation();
    })
      .on('dragover dragenter', function () {
        dropArea.addClass('dragged');
      })
      .on('dragleave dragend drop', function () {
        dropArea.removeClass('dragged');
      })
      .on('drop', function (e) {
        let files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
      });

    $("#fileInput").on('change', function () {
      let files = this.files;
      handleFiles(files);
    });

    function handleFiles(files) {
      // let x = document.getElementById("div_test");
      // var imagejavascript = document.createElement("svg");
      // var im = document.createElement("img");
      // im.src = "images.png";
      // // imagejavascript.src = "arman.svg";
      // imagejavascript.appendChild(im);
      // x.appendChild(im);

      if (files.length > 0) {
        let file = files[0];
        uploadFile(file);
        // if (file.type === 'dxf') {
        //     uploadFile(file);
        // } else {
        //     alert('Veuillez sélectionner un fichier DXF valide.');
        // }
      }
    }

    function uploadFile(file) {
      console.log(file);
      let formData = new FormData();
      formData.append('file', file);
      let imageElement = document.getElementsByClassName("img_usinage")[0];
      var selectElement = document.getElementById("epp");
      var selectedOption = selectElement.options[selectElement.selectedIndex];
      var selectedValue = selectedOption.value;

      var selectType = document.getElementById("type_usinage");
      var selectedTypeOption = selectType.options[selectType.selectedIndex];
      var selectedTypeValue = selectedTypeOption.value;

      var selectMatiereElement = document.getElementById("matiere_select");
      var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
      var mt = selectedMatiereOption.value;

      var selectMatiereTypeElement = document.getElementById("type_matiere");
      var selectedMatiereTypeOption = selectMatiereTypeElement.options[selectMatiereTypeElement.selectedIndex];
      var mt_name = selectedMatiereTypeOption.value;

      var qte = document.getElementById("qte").value;


      // var mt = document.getElementById("mt").innerText;
      // var mt_name = document.getElementById("mt_name").innerText;
      formData.append('mt', mt);
      formData.append('mt_name', mt_name);
      formData.append('selectedValue', selectedValue);
      formData.append('selectedTypeValue', selectedTypeValue);
      // formData.append('qte', qte);
      $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          // console.log(data['clients']);
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(prix_matiere_mtr);
          larg = data['dimension']['larg'] / 1000;
          long = data['dimension']['long'] / 1000;
          var path_folder = data['path_folder'];

          if (larg && long) {
            surface = (larg * long);
            // console.log(surface);
            perimetre = data['perimetre'];
          }

          // if(larg && long){
          //   surface = 2*(larg+long);
          // } else if(larg && long ==0){
          //   surface = larg;
          // } else if(long && larg == 0){
          //   surface = long;
          // }

          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          console.log(prix_matiere_ht);
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
          let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
          // console.log(prix_matiere_ht);
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


          // Change the image source
          imageElement.src = path_folder + '/current.png';
          let myDiv = document.getElementById("accordionExample");
          myDiv.style.display = "block";
          let devis_pro = document.getElementById("acardion_format_pro");
          devis_pro.style.display = "block";
          let form_envoyer_usinage_btn = document.getElementById("form_envoyer_usinage_btn");
          form_envoyer_usinage_btn.style.display= "block";
          let total_prix_detailles = document.getElementById("total_prix_detailles");
          total_prix_detailles.style.display = "flex";
          // let myDiv2 = document.getElementById("prix_total");
          // myDiv2.style.display = "block";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
        }
      });
    }
  });



  /**
 * Initiate Pure Counter 
 */
  $("#qte").on('input', function () {
    let qte = this.value;
    // alert("dqq");
    if (qte < -1) {
      // alert("d");
      this.value = 1;
    }
    document.getElementById("qte_structure").innerHTML = qte;
    let verif_file = document.getElementById("fileInput").value;
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      console.log("sd")
      console.log(parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht));
      document.getElementById("prix_lin_ht").innerHTML = qte * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht));
      document.getElementById("prix_lin_ttc").innerHTML = qte * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc));

    }
  });

  // **************
  // ****************
  if (document.getElementById('dateInput')) {
    document.getElementById('dateInput').min = new Date().toISOString().split('T')[0];
  }

  new PureCounter();

})()
function ouvrir_form_envoi() {
  let myDiv = document.getElementById("envoi_div");
  myDiv.style.display = "block";
}
function fermer_envoi() {
  let myDiv = document.getElementById("envoi_div");
  myDiv.style.display = "none";
}
function envoyer_command() {
  let formData = new FormData();

  var selectEpesseurElement = document.getElementById("epp");
  var selectEpesseuredOption = selectEpesseurElement.options[selectEpesseurElement.selectedIndex];
  var selectedEpesseurValue = selectEpesseuredOption.value;

  var selectClientElement = document.getElementById("client_select");
  console.log(selectClientElement);
  var selectedClientOption = selectClientElement.options[selectClientElement.selectedIndex];
  var selectedClientValue = selectedClientOption.value;

  var selectMatiereElement = document.getElementById("matiere_select");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var name_matiere = selectedMatiereOption.innerHTML;

  var selectTypeElement = document.getElementById("type_matiere");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var type_matiere = selectedTypeOption.innerText;


  var selectType = document.getElementById("type_usinage");
  var selectedTypeOption = selectType.options[selectType.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var prix_matiere = document.getElementById("prix_mat_ttc").innerHTML;
  var prix_limeaire = document.getElementById("frais_decoup_ttc").innerHTML;

  var qte = document.getElementById("qte").value;
  // var mt = document.getElementById("mt").innerText;
  // var mt_name = document.getElementById("mt_name").innerText;
  var name_dxf = "test";
  var date_livraison = document.getElementById("dateInput").value;
  var description = document.getElementById("descriptionInput").value;
  console.log(date_livraison);

  var statut = "en_attente";
  formData.append('client_id', selectedClientValue);
  formData.append('statut', statut);
  formData.append('name_matiere', name_matiere);
  formData.append('type_matiere', type_matiere);

  formData.append('type_usinage', selectedTypeValue);
  formData.append('count', qte);
  formData.append('prix_matiere', prix_matiere);

  formData.append('prix_limeaire', prix_limeaire);
  formData.append('name_dxf', name_dxf);
  formData.append('description', description);
  formData.append('date_fin', date_livraison);
  formData.append('epaisseur_id', selectedEpesseurValue);
  $.ajax({
    url: '/new_command',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      console.log(msg)
      let myDiv = document.getElementById("envoi_div");
      myDiv.style.display = "none";


    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function confirmation(id) {
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_confirmer',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {

      // window.location.href = "/en_attente";
      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function supprimer_attente(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_attente',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/en_attente";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });
  }

}
function supprimer_confirmé(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_confirmé',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/confirmé";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });
  }

}
function supprimer_usiné(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_usiné',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/usiné";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });
  }

}

function passe_usinage(id) {
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_usiner',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {


      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function envoie_livraison(id) {
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_livré',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      window.location.href = "/usiné";

      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}

function telecharger_pdf(user) {
  var selectDevisProElement = document.getElementById("cients_devis_pro");
  var selectDevisProOption = selectDevisProElement.options[selectDevisProElement.selectedIndex];
  var selectedDevisProValue = selectDevisProOption.value;
  let formData = new FormData();
  if (selectedDevisProValue == -1) {
    let text = "Voulez vous continuer sans client?";
    confirm(text);

  } else {
    formData.append('client_id', selectedDevisProValue);
  }


  var selectMatiereElement = document.getElementById("matiere_select");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var matiere = selectedMatiereOption.innerText;

  var selectTypeElement = document.getElementById("type_matiere");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var type_matiere = selectedTypeOption.innerText;

  var selectEpesseurElement = document.getElementById("epp");
  var selectEpesseuredOption = selectEpesseurElement.options[selectEpesseurElement.selectedIndex];
  var epp = selectEpesseuredOption.innerText;




  // var selectClientElement = document.getElementById("cient_select");
  // var selectedClientOption = selectClientElement.options[selectClientElement .selectedIndex];
  // var selectedClientValue = selectedClientOption.value;


  var selectType = document.getElementById("type_usinage");
  var selectedTypeOption = selectType.options[selectType.selectedIndex];
  var type_usinage = selectedTypeOption.innerText;

  var prix_ht = parseFloat(document.getElementById("prix_lin_ht").innerHTML);
  // var prix_limeaire = document.getElementById("frais_decoup_ttc").innerHTML;

  var qte = parseInt(document.getElementById("qte").value);
  console.log(typeof qte);



  // formData.append('client_id', selectedClientValue);
  formData.append('name_matiere', matiere);
  formData.append('type_matiere', type_matiere);

  formData.append('type_usinage', type_usinage);
  formData.append('qte', qte);
  formData.append('prix_ht', prix_ht);
  formData.append('epaisseur', epp);
  formData.append('user', user);
  $.ajax({
    url: '/telecharger_pdf',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      var link = document.createElement('a');
      console.log(link)
      link.href = 'static/members/comercial/Eric/output.pdf';  // Replace with the actual path to your PDF file.
      link.download = 'test.pdf';  // The name you want the downloaded file to have.
      document.body.appendChild(link);
      console.log(link)
      link.click();
      document.body.removeChild(link);

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function confirmation(id) {
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_confirmer',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      window.location.href = "/en_attente";

      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function usiner(id) {
  alert("d");
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_usiner',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      window.location.href = "/confirmé";

      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function text_btn_active() {

  var file_btn = document.getElementById("file_btn");
  var text_bn = document.getElementById("text_btn");

  // text_bn.classList.add("active-case");
  if (!text_bn.classList.contains("active-case")) {

    text_bn.classList.add("active-case");
    text_section = document.getElementById("text-section");
    text_section.style.display = "block"


    if (file_btn.classList.contains("active-case")) {
      file_btn.classList.remove("active-case");
      drop_area = document.getElementById("drop-area");
      drop_area.style.display = "none";
    }
  }
}

function upload_btn_active() {

  var file_btn = document.getElementById("file_btn");
  var text_bn = document.getElementById("text_btn");

  // text_bn.classList.add("active-case");
  if (!file_btn.classList.contains("active-case")) {

    file_btn.classList.add("active-case");
    drop_area = document.getElementById("drop-area");
    drop_area.style.display = "block"


    if (text_bn.classList.contains("active-case")) {
      text_bn.classList.remove("active-case");
      text_section = document.getElementById("text-section");
      text_section.style.display = "none";
    }
  }
}
function ajuter_plaque_select() {
  var myDiv = document.getElementById("plaque_div");

  // HTML code to append
  var htmlCode = `<div class=" mt-3 col-7">
  <select class="form-select" aria-label="Default select example">
      <option selected>Plaque sorti</option>
      <option value="1">4000x2000</option>
      <option value="2">3000x2000</option>
      <option value="3">4000x1500</option>
      <option value="4">3000x1500</option>
      <option value="5">4000x1000</option>
      <option value="6">3000x1000</option>
      <option value="7">4000x2000</option>
      <option value="8">3000x1250</option>
      <option value="9">2250x1250</option>
  </select>
</div>
<div class="col-4">
  <button class="btn_counter decrement_plaque">-</button>
  
  <input id="qte_plaque" value=1 min="0">
  <button class="btn_counter increment_plaque">+</button>
</div>`;

  // Append HTML using innerHTML
  myDiv.innerHTML += htmlCode;
}