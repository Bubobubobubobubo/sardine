<script>
 let htmlContent = ''
 // This is only temporary!
 fetch('https://raw.githubusercontent.com/Bubobubobubobubo/sardine/main/docs/index.html').then(response => {
	 console.dir(response)
	 return response.text();
 }).then(html => {
	 htmlContent = html
 })
</script>
<section>
    {@html htmlContent}
</section>
