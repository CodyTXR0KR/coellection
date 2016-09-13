/* Transform simple database strings to html link elements */
function makeTwitterLink(username) {
    var url = "https://twitter.com/" + username.slice(1);
    return username.link(url);
}

function getTwitterAvatar(username) {
    return "https://avatars.io/twitter/" + username.slice(1);
}

function donorOutput(donor_name) {
    if (donor_name.startsWith("@")) {
        return makeTwitterLink(donor_name);
    };
    return donor_name;
}

function populateTopDonor(input) {
    var top_donor = input.split(" ");
    var donor_name = top_donor[0];
    var donations = top_donor.slice(-1)[0];

    if (donor_name.startsWith("@")) {
        var avatar = document.getElementById("avatar");
        var link = document.getElementById("twitter_link");

        avatar.src = getTwitterAvatar(donor_name);
        avatar.alt = donor_name.slice(1);
        // link.setAttribute('href', "https://twitter.com/" + donor_name.slice(1));
        link.innerHTML = "<a href='https://twitter.com/" + donor_name.slice(1) + "'>" + donor_name + "</a>";
    };
    console.log("dynamic_links.js::populateTopDonor...done.");
}