if (document.documentElement.clientWidth < document.documentElement.scrollWidth) {
    const prof = document.getElementById("userprofile")
    prof.classList.add("pb-2")
} else {
    if (prof.classList.contains("pb-2")) {
        prof.classList.remove("pb-2")
    }
}