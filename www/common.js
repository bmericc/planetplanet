var entries = []

function toggleEntry(id) {
	// hide summary
	$("#summary_" + id).slideToggle()
	if ($("#summary_" + id).css("display") == "none") {
		// change the link text
		$("#toggle_content_" + id).text("Bu yazıyla ilgili detayları okumak için tıklayın.")
	} else {
		// change the link text
		$("#toggle_content_" + id).text("Bu yazının detaylarını kapatmak için tıklayın.")
	}
	// show the content
	$("#content_" + id).slideToggle();
}