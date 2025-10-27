1:"$Sreact.fragment"
4:I[97367,["/_next/static/chunks/ff1a16fafef87110.js","/_next/static/chunks/247eb132b7f7b574.js"],"OutletBoundary"]
5:"$Sreact.suspense"
2:T629,
          document.getElementById('contactForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            const status = document.getElementById('formStatus');
            const button = form.querySelector('button[type="submit"]');

            button.disabled = true;
            button.textContent = 'Sending...';

            try {
              const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
              });

              const result = await response.json();

              if (response.ok) {
                status.className = 'block text-center py-2 rounded-lg bg-green-500/20 text-green-400 border border-green-500/50';
                status.textContent = result.message || 'Message sent successfully!';
                form.reset();
              } else {
                throw new Error(result.error || 'Failed to send message');
              }
            } catch (error) {
              status.className = 'block text-center py-2 rounded-lg bg-red-500/20 text-red-400 border border-red-500/50';
              status.textContent = error.message || 'Something went wrong. Please try again.';
            } finally {
              button.disabled = false;
              button.textContent = 'Send Message';
            }
          });
        0:{"buildId":"VdGkSDcQmwQJTqX9PX4h0","rsc":["$","$1","c",{"children":[["$","div",null,{"className":"min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white py-24","children":["$","div",null,{"className":"container mx-auto px-4 max-w-2xl","children":[["$","h1",null,{"className":"text-4xl font-bold mb-4 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent","children":"Contact Us"}],["$","p",null,{"className":"text-gray-400 text-center mb-12","children":"Have questions? We'd love to hear from you."}],["$","div",null,{"className":"bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-8","children":["$","form",null,{"id":"contactForm","className":"space-y-6","children":[["$","div",null,{"children":[["$","label",null,{"htmlFor":"name","className":"block text-sm font-medium text-gray-300 mb-2","children":"Name"}],["$","input",null,{"type":"text","id":"name","name":"name","required":true,"className":"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors","placeholder":"Your name"}]]}],["$","div",null,{"children":[["$","label",null,{"htmlFor":"email","className":"block text-sm font-medium text-gray-300 mb-2","children":"Email"}],["$","input",null,{"type":"email","id":"email","name":"email","required":true,"className":"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors","placeholder":"your@email.com"}]]}],["$","div",null,{"children":[["$","label",null,{"htmlFor":"message","className":"block text-sm font-medium text-gray-300 mb-2","children":"Message"}],["$","textarea",null,{"id":"message","name":"message","required":true,"rows":6,"className":"w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 transition-colors resize-none","placeholder":"How can we help you?"}]]}],["$","div",null,{"id":"formStatus","className":"hidden text-center py-2 rounded-lg"}],["$","button",null,{"type":"submit","className":"w-full py-3 px-6 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg font-semibold transition-all duration-200 transform hover:scale-[1.02]","children":"Send Message"}]]}]}],["$","script",null,{"dangerouslySetInnerHTML":{"__html":"$2"}}]]}]}],null,"$L3"]}],"loading":null,"isPartial":false}
3:["$","$L4",null,{"children":["$","$5",null,{"name":"Next.MetadataOutlet","children":"$@6"}]}]
6:null
