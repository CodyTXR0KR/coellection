
function makeTwitterLink(username) {
    // Return an html twitter link to the provided username
    var url = "https://twitter.com/" + username.slice(1);
    return username.link(url);
}

function getTwitterAvatar(username) {
    // Return the img src url for a twitter user
    return "https://avatars.io/twitter/" + username.slice(1);
}

function donorOutput(donor_name) {
    // Parse template data to link html if necessary
    if (donor_name.startsWith("@")) {
        return makeTwitterLink(donor_name);
    };
    return donor_name;
}

function populateTopDonor(input) {
    // Parse template data to populate top donor div
    var top_donor = input.split(" ");
    var donor_name = top_donor[0];
    var donation_count = top_donor.slice(-1)[0];

    if (donor_name.startsWith("@")) {
        var avatar = document.getElementById("avatar_sm");
        var link = document.getElementById("twitter_link");
        var donations = document.getElementById("donations");

        avatar.src = getTwitterAvatar(donor_name);
        avatar.alt = donor_name;
        link.innerHTML = makeTwitterLink(donor_name);
        donations.innerText = donation_count + " donations!";
    };
    console.log("dynamic_links.js::populateTopDonor...done.");
}

// Scrolling contributor marquee
// reference: http://stackoverflow.com/questions/10547797/very-simple-very-smooth-javascript-marquee
function marquee(a, b) {
    var width = b.width();
    var start_pos = a.width();
    var end_pos = -width;

    function scroll() {
        if (b.position().left <= -width) {
            b.css('left', start_pos);
            scroll();
        }
        else {
            // Increase or decrease speed by changing value 50000
            // larger is slower
            time = (parseInt(b.position().left, 10) - end_pos) *
                (50000 / (start_pos - end_pos));
            b.animate({
                'left': -width
            }, time, 'linear', function() {
                scroll();
            });
        }
    }

    b.css({
        'width': width,
        'left': start_pos
    });
    scroll(a, b);

    b.mouseenter(function() {     // Remove these lines
        b.stop();                 //
        b.clearQueue();           // if you don't want
    });                           //
    b.mouseleave(function() {     // marquee to pause
        scroll(a, b);             //
    });                           // on mouse over

}

$(document).ready(function() {
    marquee($('#contributors'), $('#donor_list'));
});
$('#section_carousel').carousel({
    interval: 5000
});