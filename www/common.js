var entries = []

function toggleEntry(id) {
	if ($("#summary_" + id).css("display") == "none") {
		// change the link text
		$("#toggle_content_" + id).text("Bu yazının devamını okumak için tıklayın.")
	} else {
		// change the link text
		$("#toggle_content_" + id).text("Bu yazının devamını kapatmak için tıklayın.")
	}
	$("#content_" + id).slideToggle()
	$("#summary_" + id).slideToggle()
}